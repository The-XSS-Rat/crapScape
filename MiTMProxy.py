import tkinter as tk
from tkinter import messagebox, simpledialog

class RequestInterceptor:
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.request_history = []

    def intercept_request(self, request):
        # Display the intercepted request details in the text widget
        self.text_widget.insert(tk.END, "Intercepted Request:\n")
        self.text_widget.insert(tk.END, "URL: {}\n".format(request["url"]))
        self.text_widget.insert(tk.END, "Method: {}\n".format(request["method"]))
        self.text_widget.insert(tk.END, "Headers: {}\n".format(request["headers"]))
        self.text_widget.insert(tk.END, "Content: {}\n\n".format(request["content"]))

        # Modify the intercepted request if needed
        request["headers"]["X-Custom-Header"] = "Modified Value"
        request["content"] = "Modified Request Content"

        # Add the intercepted request to the history
        self.request_history.append(request)

    def get_request_history(self):
        return self.request_history

class ResponseInterceptor:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def intercept_response(self, response):
        # Display the intercepted response details in the text widget
        self.text_widget.insert(tk.END, "Intercepted Response:\n")
        self.text_widget.insert(tk.END, "URL: {}\n".format(response["url"]))
        self.text_widget.insert(tk.END, "Status Code: {}\n".format(response["status_code"]))
        self.text_widget.insert(tk.END, "Headers: {}\n".format(response["headers"]))
        self.text_widget.insert(tk.END, "Content: {}\n\n".format(response["content"]))

        # Modify the intercepted response if needed
        response["headers"]["X-Custom-Header"] = "Modified Value"
        response["content"] = "Modified Response Content"

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Interception Proxy")

        self.text_widget = tk.Text(self.root, state=tk.DISABLED)
        self.text_widget.pack(fill=tk.BOTH, expand=True)

        self.request_interceptor = RequestInterceptor(self.text_widget)
        self.response_interceptor = ResponseInterceptor(self.text_widget)

        self.setup_menu()

    def setup_menu(self):
        menu_bar = tk.Menu(self.root)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Request History", command=self.show_request_history)
        file_menu.add_command(label="Resend Request", command=self.resend_request)
        menu_bar.add_cascade(label="File", menu=file_menu)

        self.root.config(menu=menu_bar)

    def show_request_history(self):
        request_history = self.request_interceptor.get_request_history()
        if not request_history:
            messagebox.showinfo("Request History", "No requests intercepted yet.")
        else:
            request_urls = [request["url"] for request in request_history]
            selected_request = simpledialog.askstring("Request History", "Select a request:",
                                                      autocompletevalues=request_urls)
            if selected_request:
                for request in request_history:
                    if request["url"] == selected_request:
                        self.text_widget.config(state=tk.NORMAL)
                        self.text_widget.delete(1.0, tk.END)
                        self.text_widget.insert(tk.END, "Selected Request:\n")
                        self.text_widget.insert(tk.END, "URL: {}\n".format(request["url"]))
                        self.text_widget.insert(tk.END, "Method: {}\n".format(request["method"]))
                        self.text_widget.insert(tk.END, "Headers: {}\n".format(request["headers"]))
                        self.text_widget.insert(tk.END, "Content: {}\n\n".format(request["content"]))
                        self.text_widget.config(state=tk.DISABLED)
                        break

    def resend_request(self):
        request_history = self.request_interceptor.get_request_history()
        if not request_history:
            messagebox.showinfo("Resend Request", "No requests intercepted yet.")
        else:
            request_urls = [request["url"] for request in request_history]
            selected_request = simpledialog.askstring("Resend Request", "Select a request:",
                                                      autocompletevalues=request_urls)
            if selected_request:
                for request in request_history:
                    if request["url"] == selected_request:
                        # Add your code to resend the selected request here
                        break

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    window = MainWindow()
    window.run()
