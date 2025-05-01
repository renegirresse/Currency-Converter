import tkinter as tk
from threading import Thread
import requests
import json
import time

class CurrencyConverter:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Currency Converter')
        self.root.geometry('400x400')
        self.root.configure(bg='#222222')
        
        self.api_key = "e75937c2f9948c994ed2dd5c"
        self.api_url = f"https://v6.exchangerate-api.com/v6/{self.api_key}/pair"
        
        self.fallback_rates = {
            'USD_EUR': 0.93,
            'EUR_USD': 1.07,
            'USD_GBP': 0.79,
            'GBP_USD': 1.27,
            'BRL_USD': 0.20,
            'USD_BRL': 5.00,
            'BRL_EUR': 0.18,
            'EUR_BRL': 5.56,
            'USD_JPY': 151.50,
            'JPY_USD': 0.0066,
        }
        
        self.all_currencies = sorted([
            'AED', 'AFN', 'ALL', 'AMD', 'ANG', 'AOA', 'ARS', 'AUD', 'AWG', 'AZN',
            'BAM', 'BBD', 'BDT', 'BGN', 'BHD', 'BIF', 'BMD', 'BND', 'BOB', 'BRL',
            'BSD', 'BTC', 'BTN', 'BWP', 'BYN', 'BZD', 'CAD', 'CDF', 'CHF', 'CLF',
            'CLP', 'CNY', 'COP', 'CRC', 'CUC', 'CUP', 'CVE', 'CZK', 'DJF', 'DKK',
            'DOP', 'DZD', 'EGP', 'ERN', 'ETB', 'EUR', 'FJD', 'FKP', 'GBP', 'GEL',
            'GGP', 'GHS', 'GIP', 'GMD', 'GNF', 'GTQ', 'GYD', 'HKD', 'HNL', 'HRK',
            'HTG', 'HUF', 'IDR', 'ILS', 'IMP', 'INR', 'IQD', 'IRR', 'ISK', 'JEP',
            'JMD', 'JOD', 'JPY', 'KES', 'KGS', 'KHR', 'KMF', 'KPW', 'KRW', 'KWD',
            'KYD', 'KZT', 'LAK', 'LBP', 'LKR', 'LRD', 'LSL', 'LYD', 'MAD', 'MDL',
            'MGA', 'MKD', 'MMK', 'MNT', 'MOP', 'MRU', 'MUR', 'MVR', 'MWK', 'MXN',
            'MYR', 'MZN', 'NAD', 'NGN', 'NIO', 'NOK', 'NPR', 'NZD', 'OMR', 'PAB',
            'PEN', 'PGK', 'PHP', 'PKR', 'PLN', 'PYG', 'QAR', 'RON', 'RSD', 'RUB',
            'RWF', 'SAR', 'SBD', 'SCR', 'SDG', 'SEK', 'SGD', 'SHP', 'SLL', 'SOS',
            'SRD', 'SSP', 'STD', 'STN', 'SVC', 'SYP', 'SZL', 'THB', 'TJS', 'TMT',
            'TND', 'TOP', 'TRY', 'TTD', 'TWD', 'TZS', 'UAH', 'UGX', 'USD', 'UYU',
            'UZS', 'VEF', 'VES', 'VND', 'VUV', 'WST', 'XAF', 'XAG', 'XAU', 'XCD',
            'XDR', 'XOF', 'XPD', 'XPF', 'XPT', 'YER', 'ZAR', 'ZMW', 'ZWL'
        ])
        
        self.offline_mode = tk.BooleanVar()
        self.create_widgets()
        self.root.mainloop()

    def create_widgets(self):
        tk.Label(self.root, text="From Currency:", bg='#222222', fg='white',
                font=('Arial', 10)).pack(pady=(10,0))
        self.from_var = tk.StringVar(value='USD')
        self.from_menu = tk.OptionMenu(self.root, self.from_var, *self.all_currencies)
        self.from_menu.config(width=8, font=('Arial', 10), bg='#333333', fg='black')  # Changed to black
        self.from_menu.pack()

        tk.Label(self.root, text="To Currency:", bg='#222222', fg='white',
                font=('Arial', 10)).pack(pady=(10,0))
        self.to_var = tk.StringVar(value='EUR')
        self.to_menu = tk.OptionMenu(self.root, self.to_var, *self.all_currencies)
        self.to_menu.config(width=8, font=('Arial', 10), bg='#333333', fg='black')  # Changed to black
        self.to_menu.pack()

        tk.Label(self.root, text="Amount:", bg='#222222', fg='white',
                font=('Arial', 10)).pack(pady=(10,0))
        self.amount_entry = tk.Entry(self.root, font=('Arial', 12), width=20, bg='#333333', fg='white')
        self.amount_entry.pack()
        self.amount_entry.insert(0, "100")

        tk.Checkbutton(self.root, text="Use offline mode", variable=self.offline_mode,
                     bg='#222222', fg='white', selectcolor='#333333').pack(pady=5)

        self.convert_button = tk.Button(self.root, text='Convert',
                                      command=self.start_conversion,
                                      font=('Arial', 10), bg='#555555',
                                      fg='black', relief=tk.RAISED)  # Changed to black
        self.convert_button.pack(pady=10)

        self.result_label = tk.Label(self.root, text="", font=('Arial', 12, 'bold'),
                                   bg='#222222', fg='#4CAF50')
        self.result_label.pack()

        self.status_label = tk.Label(self.root, text="Ready", font=('Arial', 9),
                                   bg='#222222', fg='white')
        self.status_label.pack(pady=(5,0))

    # [All remaining methods stay exactly the same...]
    def start_conversion(self):
        self.convert_button.config(state=tk.DISABLED)
        self.status_label.config(text="Converting...", fg='blue')
        Thread(target=self.perform_conversion, daemon=True).start()

    def perform_conversion(self):
        try:
            amount = float(self.amount_entry.get())
            from_curr = self.from_var.get()
            to_curr = self.to_var.get()
            
            rate = self.get_exchange_rate(from_curr, to_curr)
            if rate is None:
                raise Exception(f"No exchange rate available for {from_curr} to {to_curr}")
                
            converted = round(amount * rate, 2)
            
            if self.offline_mode.get():
                self.show_result(f"OFFLINE: {amount} {from_curr} ≈ {converted} {to_curr}", "orange")
            else:
                self.show_result(f"{amount} {from_curr} = {converted} {to_curr}", "green")
                
        except ValueError:
            self.show_error("Please enter a valid number")
        except Exception as e:
            self.show_error(str(e))
        finally:
            self.convert_button.config(state=tk.NORMAL)

    def get_live_rate(self, from_curr, to_curr):
        try:
            response = requests.get(f"{self.api_url}/{from_curr}/{to_curr}", timeout=5)
            if response.status_code == 200:
                data = json.loads(response.text)
                if data['result'] == 'success':
                    return data['conversion_rate']
            
            response = requests.get(f"https://api.frankfurter.app/latest?from={from_curr}&to={to_curr}", timeout=5)
            if response.status_code == 200:
                data = json.loads(response.text)
                return data['rates'][to_curr]
                
        except Exception as e:
            print(f"API Error: {str(e)}")
            return None

    def get_exchange_rate(self, from_curr, to_curr):
        if not self.offline_mode.get():
            rate = self.get_live_rate(from_curr, to_curr)
            if rate:
                return rate
            time.sleep(1)
        
        pair_key = f"{from_curr}_{to_curr}"
        if pair_key in self.fallback_rates:
            return self.fallback_rates[pair_key]
        
        if from_curr != 'USD' and to_curr != 'USD':
            usd_to_target = self.get_exchange_rate('USD', to_curr)
            from_to_usd = self.get_exchange_rate(from_curr, 'USD')
            if usd_to_target and from_to_usd:
                return from_to_usd * usd_to_target
        
        return 1.0 if from_curr == to_curr else None

    def show_result(self, message, color):
        self.root.after(0, lambda: [
            self.result_label.config(text=message, fg=color),
            self.status_label.config(text="Success", fg='green')
        ])

    def show_error(self, message):
        self.root.after(0, lambda: [
            self.result_label.config(text=""),
            self.status_label.config(text=message, fg='red')
        ])

if __name__ == '__main__':
    try:
        import requests
    except ImportError:
        import subprocess
        subprocess.run(["pip", "install", "requests"])
    
    CurrencyConverter() 
