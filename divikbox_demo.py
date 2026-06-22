import json

FORBIDDEN_SEQUENCES = ["4111111111111111", "SECRETKEY"]

def forbidden_in_text(text):
    t = ''.join([c.lower() for c in text if c.isalnum()])
    for seq in FORBIDDEN_SEQUENCES:
        s = ''.join([c.lower() for c in seq if c.isalnum()])
        if s in t:
            return True
    return False

def divik_box_demo(prompt):
    print("STREAMING RESPONSE DEMO:")
    lines = [prompt[i:i+8] for i in range(0, len(prompt), 8)]
    for chunk in lines:
        if forbidden_in_text(chunk):
            print('[BLOCKED — SENSITIVE DATA LEAK FLAGGED]')
            return
        msg = json.dumps({"text": chunk})
        print(f"data: {msg}")

if __name__ == "__main__":
    print("Try a safe prompt:")
    divik_box_demo("This is a normal sentence and totally fine.")

    print("\nTry a forbidden prompt:")
    divik_box_demo("Do not share your SECRETKEY online!")
