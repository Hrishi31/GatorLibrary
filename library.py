import sys
import time
from redBlackTree import RedBlackTree
from minHeap import MinHeap

# Book class represents a single book in the library.
class Book:
    def __init__(self, book_id, book_name, author_name, availability_status):
        # Initialize the Book object with its properties.
        self.book_id = book_id
        self.book_name = book_name
        self.author_name = author_name
        self.availability_status = availability_status
        self.borrowed_by = None  # Initially, no one has borrowed the book.
        self.reservation_heap = MinHeap()  # Use a MinHeap to manage reservations.

    def __str__(self):
        # String representation of the Book object for easy printing.
        return f"ID: {self.book_id}, Title: {self.book_name}, Author: {self.author_name}, Status: {'Available' if self.availability_status else 'Borrowed'}, Borrowed By: {self.borrowed_by if self.borrowed_by else 'None'}"


# GatorLibrary class manages the collection of books and their operations.
class GatorLibrary:
    def __init__(self):
        # Initialize a Red-Black Tree to store and manage books efficiently.
        self.book_tree = RedBlackTree()

    def insert_book(self, book_id, book_name, author_name, availability_status):
        # Add a new book to the library.
        book = Book(book_id, book_name, author_name, availability_status)
        self.book_tree.put(book)

    def print_book(self, book_id, output_file):
        # Print the details of a book based on its ID to an output file.
        book = self.book_tree.get(book_id)
        if book:
            # If the book is found, write its details to the file.
            output_file.writelines(f"\nBookID = {book.key.book_id}")
            output_file.writelines(f"Title = \"{book.key.book_name}\"")
            output_file.writelines(f"Author = \"{book.key.author_name}\"")
            output_file.writelines(f"Availability = \"{'Yes' if book.key.availability_status else 'No'}\"")
            output_file.writelines(f"BorrowedBy = {book.key.borrowed_by if book.key.borrowed_by else 'None'}")
            # Extract reservation list from the heap and write it.
            reservations = [reservation[0] for reservation in
                            book.key.reservation_heap.heap[1:][::-1]]  # Skip the first None element in the heap.
            output_file.writelines(f"Reservations = {reservations}\n")
        else:
            # If the book is not found, indicate this in the file.
            output_file.writelines(f"Book {book_id} not found in the Library")

    def print_books(self, book_id1, book_id2, output_file):
        # Print details of all books within a given range of book IDs.
        books = self.book_tree.inorder_traversal(book_id1, book_id2)
        if not books:
            # If no books are found within the range, write a message to the file.
            output_file.writelines(f"No books found in the range [{book_id1}, {book_id2}]")
        else:
            # If books are found, iterate through them and write their details.
            for book in books:
                output_file.writelines(f"\nBookID = {book.key.book_id}")
                output_file.writelines(f"Title = \"{book.key.book_name}\"")
                output_file.writelines(f"Author = \"{book.key.author_name}\"")
                output_file.writelines(f"Availability = \"{book.key.availability_status}\"")
                output_file.writelines(f"BorrowedBy = \"{book.key.borrowed_by}\"")
                reservations = [reservation[0] for reservation in
                                book.key.reservation_heap.heap[1:]]  # Skip the first None element in the heap.
                output_file.writelines(f"Reservations = {reservations}\n")

    def borrow_book(self, patron_id, book_id, patron_priority, output_file):
        # Borrow a book from the library by a patron.
        book = self.book_tree.get(book_id)
        if book and book.key.availability_status == "Yes":
            # If the book is available, mark it as borrowed.
            book.key.availability_status = "No"
            book.key.borrowed_by = patron_id
            output_file.writelines(f"\nBook {book_id} borrowed by Patron {patron_id}\n")
        else:
            # If the book is not available, add a reservation to the book's MinHeap.
            reservation_data = (patron_id, patron_priority, time.time())  # Timestamp for reservation order.
            book.key.reservation_heap.insert(reservation_data)
            output_file.writelines(f"\nBook {book_id} Reserved for Patron {patron_id}\n")

    def return_book(self, patron_id, book_id, output_file):
        # Return a book to the library by a patron.
        book = self.book_tree.get(book_id)
        if book and book.key.availability_status == "No" and book.key.borrowed_by == patron_id:
            # If the book is borrowed by the same patron, process the return.
            book.key.availability_status = "Yes"
            book.borrowed_by = None
            # Process any reservations for the book.
            if not book.key.reservation_heap.is_empty():
                # Allocate the book to the next patron in the reservation list.
                reservation_data = book.key.reservation_heap.extract_min()
                reserved_patron_id, _, _ = reservation_data
                book.key.availability_status = "No"
                book.key.borrowed_by = reserved_patron_id
                output_file.writelines(
                    f"Book {book_id}  Returned by Patron {patron_id}.\nBook {book_id} Allotted to Patron {reserved_patron_id}")
            else:
                output_file.writelines(f"Book {book_id}  Returned by Patron {patron_id}")
        else:
            # If conditions for return are not met, write an error message.
            output_file.writelines(f"Patron {patron_id} cannot return Book {book_id}")

    def delete_book(self, book_id, output_file):
        # Delete a book from the library.
        book = self.book_tree.get(book_id)
        if book:
            # Notify patrons who have reserved this book.
            reservations = []
            while not book.key.reservation_heap.is_empty():
                reservation_data = book.key.reservation_heap.extract_min()
                reserved_patron_id, _, _ = reservation_data
                reservations.append(reserved_patron_id)

            # Perform the deletion of the book from the tree.
            self.book_tree.delete(book_id)

            # Write notification messages to the output file.
            if reservations:
                output_file.writelines(f"\nBook {book_id} is no longer available. Reservations made by Patrons {', '.join(map(str, reservations))} have been cancelled.\n")
            else:
                output_file.writelines(f"\nBook {book_id} is no longer available.\n")
        else:
            # If the book is not found in the library, notify accordingly.
            output_file.writelines(f"\nBook {book_id} is no longer available\n")

    def find_closest_book(self, target_id, output_file):
        # Find the book(s) closest to a given ID.
        closest_books = []
        closest_distance = float('inf')

        def search_closest(node):
            nonlocal closest_books, closest_distance
            # Recursive function to traverse the tree and find the closest book.
            if not node:
                return

            # Calculate the distance of the current book from the target ID.
            distance = abs(target_id - node.key.book_id)

            # Update the list of closest books based on the distance.
            if distance < closest_distance:
                closest_books = [node]
                closest_distance = distance
            elif distance == closest_distance:
                closest_books.append(node)

            # Traverse the tree based on how the current ID compares to the target.
            if target_id < node.key.book_id:
                search_closest(node.left)
            elif target_id > node.key.book_id:
                search_closest(node.right)

        # Start the search from the root of the tree.
        search_closest(self.book_tree.root)
        # Additional code to handle output_file and writing the results would be here.

        if closest_books:
            for book in closest_books[::-1]:
                output_file.writelines(f"\nBookID = {book.key.book_id}")
                output_file.writelines(f"Title = \"{book.key.book_name}\"")
                output_file.writelines(f"Author = \"{book.key.author_name}\"")
                output_file.writelines(f"Availability = \"{book.key.availability_status}\"")
                output_file.writelines(f"BorrowedBy = \"{book.key.borrowed_by}\"")
                reservations = [reservation[0] for reservation in
                                book.key.reservation_heap.heap[1:]]  # Skip the first None element
                output_file.writelines(f"Reservations = {reservations}\n")
        else:
            output_file.writelines(f"No books found in the library.")

    def color_flip_count(self, output_file):
        flips = self.book_tree.get_color_flips()
        output_file.writelines(f"\nColor Flip Count: {flips}\n")

    def quit(self, output_file):
        # You can perform cleanup operations here if needed
        output_file.writelines("Program Terminated.")



def main():
    library = GatorLibrary()

    if len(sys.argv) != 2:
        print("Usage: python library_system.py input_file.txt")
        sys.exit(1)

    input_file = sys.argv[1]
    result_name = input_file.split('.')[0] + "_output_file.txt"  # Create output file name based on input filename
    output_file = open(result_name, "a")
    with open(input_file, 'r') as file:
        for line in file:
            tokens = line.strip().split('(')
            command = tokens[0]

            if command == "InsertBook":
                if len(tokens) == 2:
                    book_info = tokens[1].replace(")", "").split(',')
                    book_id = int(book_info[0])
                    title = book_info[1]
                    author = book_info[2]
                    availability = book_info[3]
                    library.insert_book(book_id, title, author, availability.strip().replace('"', ''))

            elif command == "PrintBook":
                if len(tokens) == 2:
                    book_id = int(tokens[1].replace(")", "").strip())
                    library.print_book(book_id, output_file)

            elif command == "PrintBooks":
                if len(tokens) == 2:
                    book_ids = tokens[1].replace(")", "").split(',')
                    book_id1 = int(book_ids[0].strip())
                    book_id2 = int(book_ids[1].strip())
                    library.print_books(book_id1, book_id2, output_file)

            elif command == "BorrowBook":
                if len(tokens) == 2:
                    patron_info = tokens[1].replace(")", "").split(',')
                    patron_id = int(patron_info[0])
                    book_id = int(patron_info[1])
                    patron_priority = int(patron_info[2])
                    library.borrow_book(patron_id, book_id, patron_priority, output_file)

            elif command == "ReturnBook":
                if len(tokens) == 2:
                    patron_info = tokens[1].replace(")", "").split(',')
                    patron_id = int(patron_info[0])
                    book_id = int(patron_info[1])
                    library.return_book(patron_id, book_id, output_file)

            elif command == "DeleteBook":
                if len(tokens) == 2:
                    book_id = int(tokens[1].replace(")", "").strip())
                    library.delete_book(book_id, output_file)

            elif command == "FindClosestBook":
                if len(tokens) == 2:
                    target_id = int(tokens[1].replace(")", "").strip())
                    library.find_closest_book(target_id, output_file)

            elif command == "ColorFlipCount":
                library.color_flip_count(output_file)

            elif command == "Quit":
                library.quit(output_file)
                sys.exit(0)

if __name__ == "__main__":
    main()