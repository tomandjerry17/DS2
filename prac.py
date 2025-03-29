import random
from collections import Counter
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

class NumberFrequencyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Frequency Analyzer")
        self.root.geometry("900x700")
        
        # Configuration
        self.rows = 25
        self.cols = 40
        self.total_numbers = self.rows * self.cols
        self.min_num = 1
        self.max_num = 45
        self.numbers = []
        self.counter = None
        
        # Create UI elements
        self.create_widgets()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Number Frequency Analyzer", font=('Helvetica', 14, 'bold'))
        title_label.pack(pady=10)
        
        # Description
        desc_label = ttk.Label(main_frame, 
                             text=f"Click the button to generate {self.total_numbers} random numbers\n(between {self.min_num} and {self.max_num}) and analyze frequencies.",
                             justify=tk.CENTER)
        desc_label.pack(pady=10)
        
        # Generate button
        self.generate_btn = ttk.Button(main_frame, text="Generate & Analyze Numbers", command=self.generate_and_analyze)
        self.generate_btn.pack(pady=20)
        
        # Notebook (Tabbed interface)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab 1: Top 6 Results
        self.create_top6_tab()
        
        # Tab 2: All Random Numbers
        self.create_all_numbers_tab()
        
        # Tab 3: Sorted Frequencies
        self.create_sorted_frequencies_tab()
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Ready to generate numbers.", foreground="blue")
        self.status_label.pack(pady=10)
        
    def create_top6_tab(self):
        tab1 = ttk.Frame(self.notebook)
        self.notebook.add(tab1, text="Top 6 Results")
        
        # Treeview for displaying top 6 results
        self.top6_tree = ttk.Treeview(tab1, columns=('Rank', 'Number', 'Frequency'), show='headings')
        self.top6_tree.heading('Rank', text='Rank')
        self.top6_tree.heading('Number', text='Number')
        self.top6_tree.heading('Frequency', text='Frequency')
        self.top6_tree.column('Rank', width=50, anchor=tk.CENTER)
        self.top6_tree.column('Number', width=100, anchor=tk.CENTER)
        self.top6_tree.column('Frequency', width=100, anchor=tk.CENTER)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(tab1, orient=tk.VERTICAL, command=self.top6_tree.yview)
        self.top6_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.top6_tree.pack(fill=tk.BOTH, expand=True)
        
    def create_all_numbers_tab(self):
        tab2 = ttk.Frame(self.notebook)
        self.notebook.add(tab2, text="All Random Numbers")
        
        # ScrolledText for displaying all numbers
        self.all_numbers_text = scrolledtext.ScrolledText(
            tab2, 
            wrap=tk.WORD, 
            width=80, 
            height=25,
            font=('Consolas', 10)  # Monospaced font for alignment
        )
        self.all_numbers_text.pack(fill=tk.BOTH, expand=True)
        
    def create_sorted_frequencies_tab(self):
        tab3 = ttk.Frame(self.notebook)
        self.notebook.add(tab3, text="All Sorted Frequencies")
        
        # Treeview for displaying all frequencies
        self.freq_tree = ttk.Treeview(tab3, columns=('Number', 'Frequency'), show='headings')
        self.freq_tree.heading('Number', text='Number')
        self.freq_tree.heading('Frequency', text='Frequency')
        self.freq_tree.column('Number', width=100, anchor=tk.CENTER)
        self.freq_tree.column('Frequency', width=100, anchor=tk.CENTER)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(tab3, orient=tk.VERTICAL, command=self.freq_tree.yview)
        self.freq_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.freq_tree.pack(fill=tk.BOTH, expand=True)
        
    def generate_and_analyze(self):
        try:
            self.generate_btn.config(state=tk.DISABLED)
            self.status_label.config(text="Generating and analyzing numbers...", foreground="blue")
            self.root.update()  # Force UI update
            
            # Generate random numbers
            self.numbers = [random.randint(self.min_num, self.max_num) for _ in range(self.total_numbers)]
            
            # Count occurrences
            self.counter = Counter(self.numbers)
            
            # Update all displays
            self.update_top6_display()
            self.update_all_numbers_display()
            self.update_sorted_frequencies_display()
            
            self.status_label.config(text="Analysis complete. Results available in all tabs.", foreground="green")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.status_label.config(text="Error occurred during generation.", foreground="red")
        finally:
            self.generate_btn.config(state=tk.NORMAL)
    
    def update_top6_display(self):
        # Clear previous results
        for item in self.top6_tree.get_children():
            self.top6_tree.delete(item)
            
        # Get top 6 and insert
        top_6 = self.counter.most_common(6)
        for rank, (num, freq) in enumerate(top_6, 1):
            self.top6_tree.insert('', tk.END, values=(rank, num, freq))
    
    def update_all_numbers_display(self):
        self.all_numbers_text.delete(1.0, tk.END)
        
        # Format numbers in grid
        grid_text = ""
        for i in range(self.rows):
            row_numbers = self.numbers[i * self.cols : (i + 1) * self.cols]
            row_text = ", ".join(f"{num:2}" for num in row_numbers)
            grid_text += row_text + "\n"
        
        self.all_numbers_text.insert(tk.END, grid_text)
        self.all_numbers_text.configure(state='disabled')  # Make read-only
    
    def update_sorted_frequencies_display(self):
        # Clear previous results
        for item in self.freq_tree.get_children():
            self.freq_tree.delete(item)
            
        # Sort all frequencies (descending)
        sorted_counts = sorted(self.counter.items(), key=lambda x: (-x[1], x[0]))
        
        # Insert all
        for num, freq in sorted_counts:
            self.freq_tree.insert('', tk.END, values=(num, freq))

if __name__ == "__main__":
    root = tk.Tk()
    app = NumberFrequencyApp(root)
    root.mainloop()