import tkinter as tk
from tkinter import ttk, filedialog
import threading
import whisper
import time

class TranscriptorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Whisper Transcription App")
        self.root.geometry("600x450")

        self.audio_path = tk.StringVar()
        self.selected_model = tk.StringVar(value="small")
        self.selected_language = tk.StringVar(value="spanish")
        self.translate_to_english = tk.BooleanVar(value=False)
        self.progress_var = tk.DoubleVar()

        self.setup_ui()

    def setup_ui(self):
        # Input Section
        input_frame = ttk.LabelFrame(self.root, text="Input")
        input_frame.pack(padx=10, pady=5, fill="x")

        ttk.Label(input_frame, text="Audio file:").pack(side="left", padx=5, pady=5)
        ttk.Entry(input_frame, textvariable=self.audio_path, width=50).pack(side="left", padx=5, pady=5, expand=True, fill="x")
        ttk.Button(input_frame, text="Select audio file", command=self.select_audio_file).pack(side="right", padx=5, pady=5)

        # Model and Language Section
        settings_frame = ttk.LabelFrame(self.root, text="Settings")
        settings_frame.pack(padx=10, pady=5, fill="x")

        # Model selection
        ttk.Label(settings_frame, text="Select model:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        model_options = ["tiny", "base", "small", "medium", "large"]
        model_menu = ttk.Combobox(settings_frame, textvariable=self.selected_model, values=model_options)
        model_menu.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Language selection
        ttk.Label(settings_frame, text="Specify language:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        language_options = ["spanish", "english", "french", "german", "auto"] # Example list
        language_menu = ttk.Combobox(settings_frame, textvariable=self.selected_language, values=language_options)
        language_menu.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Translation option
        ttk.Checkbutton(settings_frame, text="Translate into English", variable=self.translate_to_english).grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="w")

        # Progress Section
        progress_frame = ttk.LabelFrame(self.root, text="Progress")
        progress_frame.pack(padx=10, pady=5, fill="x")
        
        self.progressbar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progressbar.pack(fill="x", padx=5, pady=5)
        
        self.status_label = ttk.Label(progress_frame, text="Ready.")
        self.status_label.pack(fill="x", padx=5, pady=5)

        # Transcribe Button
        ttk.Button(self.root, text="Transcribe", command=self.start_transcription).pack(pady=10)

        # Output Section
        output_frame = ttk.LabelFrame(self.root, text="Output")
        output_frame.pack(padx=10, pady=5, fill="both", expand=True)

        self.output_text = tk.Text(output_frame, wrap="word")
        self.output_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        ttk.Button(output_frame, text="Save as Text File", command=self.save_text_file).pack(side="right", padx=5, pady=5)

    def select_audio_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.flac *.wav")])
        if file_path:
            self.audio_path.set(file_path)

    def start_transcription(self):
        # Use a thread to avoid freezing the GUI
        thread = threading.Thread(target=self.run_transcription)
        thread.start()

    def run_transcription(self):
        audio_file = self.audio_path.get()
        if not audio_file:
            self.status_label.config(text="Please select an audio file first.")
            return

        model_name = self.selected_model.get()
        language = self.selected_language.get()
        translate = self.translate_to_english.get()

        self.status_label.config(text="Loading model...")
        self.progressbar.config(mode="indeterminate")
        self.progressbar.start()

        start_time = time.time()

        try:
            model = whisper.load_model(model_name)
            self.status_label.config(text="Transcribing audio...")
            
            # The transcribe method doesn't have a built-in progress bar
            # A more advanced implementation would require a custom progress handler
            result = model.transcribe(audio_file, language=language, task="translate" if translate else "transcribe")
            
            end_time = time.time()
            elapsed_time = end_time - start_time
            
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, result["text"])
            self.status_label.config(text=f"Progress: The system has completed processing.\nElapsed Time: {elapsed_time:.2f} seconds")

        except Exception as e:
            self.status_label.config(text=f"An error occurred: {e}")
        finally:
            self.progressbar.stop()
            self.progressbar.config(mode="determinate", value=0)

    def save_text_file(self):
        text_content = self.output_text.get("1.0", tk.END)
        if text_content.strip():
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
            if file_path:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(text_content)

if __name__ == "__main__":
    root = tk.Tk()
    app = TranscriptorApp(root)
    root.mainloop()