from textnode import TextNode, TextType

def main():
    # Create a TextNode with dummy values
    node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    
    # Print the object to verify the __repr__ output
    print(node)

if __name__ == "__main__":
    main()