import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox


def clear_screen():
    command = "cls" if os.name == "nt" else "clear"
    os.system(command)


def get_number(prompt):
    while True:
        text = input(prompt).strip()
        if text.lower() in {"q", "quit", "exit"}:
            return None
        try:
            return float(text)
        except ValueError:
            print("请输入有效的数字，或输入 q 退出。")


def get_choice():
    valid = {"1": "加法", "2": "减法", "3": "乘法", "4": "除法", "q": "退出"}
    while True:
        print("请选择运算：")
        print("  1) 加法        2) 减法")
        print("  3) 乘法        4) 除法")
        print("  q) 退出程序")
        choice = input("输入选项：").strip().lower()
        if choice in valid:
            return choice
        print("无效选项，请重新输入。\n")


def calculate(a, b, op):
    if op == "1":
        return a + b, "+"
    if op == "2":
        return a - b, "-"
    if op == "3":
        return a * b, "*"
    if op == "4":
        return a / b, "/"
    return None, "?"


def calculator():
    while True:
        clear_screen()
        print("==============================")
        print("        现代化计算器        ")
        print("==============================\n")
        print("提示：输入 q 可随时退出。\n")

        choice = get_choice()
        if choice == "q":
            print("感谢使用，再见！")
            break

        a = get_number("请输入第一个数字：")
        if a is None:
            print("已退出。")
            break

        b = get_number("请输入第二个数字：")
        if b is None:
            print("已退出。")
            break

        if choice == "4" and b == 0:
            print("\n错误：除数不能为 0。")
        else:
            result, symbol = calculate(a, b, choice)
            print(f"\n结果：{a} {symbol} {b} = {result}")

        print("\n按 Enter 继续，或输入 q 退出。")
        next_step = input().strip().lower()
        if next_step == "q":
            print("感谢使用，再见！")
            break


def gui_calculator():
    # hide Windows console if present, so GUI looks native (works when run with python)
    if os.name == 'nt':
        try:
            import ctypes
            hwnd = ctypes.windll.kernel32.GetConsoleWindow()
            if hwnd:
                ctypes.windll.user32.ShowWindow(hwnd, 0)
        except Exception:
            pass

    # create a modern dark window with a frosted-like effect
    try:
        import ttkbootstrap as tb  # type: ignore
        from ttkbootstrap import ttk as tbttk  # type: ignore
        use_tb = True
    except Exception:
        tb = None
        tbttk = None
        use_tb = False

    if use_tb:
        # prefer a very dark theme when available
        try:
            root = tb.Window(themename="cyborg")
        except Exception:
            root = tb.Window(themename="darkly")
        style = tb.Style()
    else:
        root = tk.Tk()

    root.title("现代化计算器")
    root.geometry("480x300")
    root.resizable(False, False)

    # prefer near-black background for stronger dark appearance
    try:
        root.configure(bg="#000000")
    except Exception:
        pass

    # transparency to simulate frosted glass (real blur not portable)
    try:
        root.attributes('-alpha', 0.94)
    except Exception:
        pass

    # background frame (card) to mimic frosted panel
    if use_tb:
        card = tbttk.Frame(root, bootstyle="secondary", padding=16)
        card.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    else:
        card = ttk.Frame(root, padding=16)
        card.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    label_font = (None, 11)
    entry_font = (None, 14)

    if use_tb:
        ttk_label = tbttk.Label
        ttk_entry = tbttk.Entry
        ttk_btn = tbttk.Button
    else:
        ttk_label = ttk.Label
        ttk_entry = ttk.Entry
        ttk_btn = ttk.Button

    ttk_label(card, text="输入表达式：例如 12+34*2，按 Enter 计算", font=label_font).grid(column=0, row=0, columnspan=2, sticky=tk.W)
    expr = ttk_entry(card, width=28, font=entry_font)
    expr.grid(column=0, row=1, columnspan=2, sticky=tk.EW)
    expr.focus()

    result_var = tk.StringVar(value="结果将在此显示")
    res_lbl = ttk_label(card, textvariable=result_var, font=(None, 13, "bold"))
    res_lbl.grid(column=0, row=2, columnspan=2, pady=(14, 0))


    def do_calc(event=None):
        expression = expr.get().strip()
        if not expression:
            return
        try:
            # only allow digits, operators and decimal point
            if not all(ch in "0123456789.+-*/() " for ch in expression):
                raise ValueError
            result = eval(expression, {"__builtins__": None}, {})
            result_var.set(f"{expression} = {result}")
        except ZeroDivisionError:
            messagebox.showerror("错误", "除数不能为 0")
        except Exception:
            messagebox.showerror("输入错误", "表达式无效，请检查后重试")


    btn_frame = ttk.Frame(card)
    btn_frame.grid(column=0, row=3, columnspan=2, pady=(18, 0))
    if use_tb:
        calc_btn = ttk_btn(btn_frame, text="计算 (Enter)", bootstyle="success", command=do_calc)
        clear_btn = ttk_btn(btn_frame, text="清除 (Ctrl+L)", bootstyle="warning", command=lambda: (expr.delete(0, tk.END), result_var.set("结果将在此显示")))
        exit_btn = ttk_btn(btn_frame, text="退出 (Esc)", bootstyle="danger", command=root.destroy)
    else:
        calc_btn = ttk_btn(btn_frame, text="计算 (Enter)", command=do_calc)
        clear_btn = ttk_btn(btn_frame, text="清除 (Ctrl+L)", command=lambda: (expr.delete(0, tk.END), result_var.set("结果将在此显示")))
        exit_btn = ttk_btn(btn_frame, text="退出 (Esc)", command=root.destroy)

    calc_btn.pack(side=tk.LEFT, padx=8)
    clear_btn.pack(side=tk.LEFT, padx=8)
    exit_btn.pack(side=tk.LEFT, padx=8)

    # keyboard shortcuts
    root.bind('<Return>', do_calc)
    root.bind('<Escape>', lambda e: root.destroy())
    root.bind('<Control-l>', lambda e: (expr.delete(0, tk.END), result_var.set("结果将在此显示")))

    for child in card.winfo_children():
        child.grid_configure(padx=8, pady=8)

    if not use_tb:
        print("提示：安装 'ttkbootstrap' 可获得更现代的毛玻璃主题（pip install ttkbootstrap）。")

    root.mainloop()


if __name__ == "__main__":
    if "--cli" in sys.argv:
        calculator()
    else:
        try:
            gui_calculator()
        except Exception as e:
            print("无法启动 GUI，已回退到命令行。错误：", e)
            calculator()
