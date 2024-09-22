# libre office

# /opt/libreoffice5.4/program/python event_6.py
# please run the below command in terminal before running the .py file 
# /opt/libreoffice5.4/program/soffice.bin "--accept=socket,host=localhost,port=2002;urp;"



import os
import uno
import time

def connect_to_libreoffice():
    """Connect to the running instance of LibreOffice."""
    local_context = uno.getComponentContext()
    resolver = local_context.ServiceManager.createInstanceWithContext(
        "com.sun.star.bridge.UnoUrlResolver", local_context)

    # Connect to the LibreOffice service
    context = resolver.resolve(
        "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")

    desktop = context.ServiceManager.createInstanceWithContext(
        "com.sun.star.frame.Desktop", context)

    return desktop


def create_and_save_odt_file(file_path):
    """Create a blank ODT document and save it to the specified path."""
    # Convert relative path to absolute path
    absolute_path = os.path.abspath(file_path)

    # Convert path to file:// format
    url = uno.systemPathToFileUrl(absolute_path)

    # Connect to LibreOffice
    desktop = connect_to_libreoffice()

    # Create a blank document
    document = desktop.loadComponentFromURL("private:factory/swriter", "_blank", 0, ())

    # Insert initial text content
    current_time_str = time.strftime("%Y-%m-%d %H:%M:%S")
    text_to_insert = "This is the text inserted at {}\n".format(current_time_str)
    insert_text(document, text_to_insert)

    # Save the document to the specified path
    property_value = uno.createUnoStruct("com.sun.star.beans.PropertyValue")
    property_value.Name = "FilterName"
    property_value.Value = "writer8"  # Internal identifier for OpenDocument Text

    properties = (property_value,)
    document.storeAsURL(url, properties)

    print("Document saved to: {}".format(file_path))
    return document


def insert_text(document, text):
    """Insert text into the document."""
    text_obj = document.Text
    cursor = text_obj.createTextCursor()
    text_obj.insertString(cursor, text, 0)


def insert_text_for_duration(document, text_prefix, duration_seconds):
    """Continuously insert text for the specified duration."""
    start_time = time.time()
    while time.time() - start_time < duration_seconds:
        current_time_str = time.strftime("%Y-%m-%d %H:%M:%S")
        text_to_insert = "{}{}\n".format(text_prefix, current_time_str)  # Add newline
        insert_text(document, text_to_insert)
        time.sleep(1)  # Wait 1 second before inserting the next text


def close_libreoffice_document(document, save_changes=False):
    """Close the LibreOffice document and save changes if needed."""
    document.close(save_changes)


def libreoffice_uno():
    """Main function to create a blank ODT file, insert text, and close the document."""
    file_path = "./extra_data/office/test_office.odt"  # Use absolute address.
    text_prefix = "This is the text inserted at "

    # Create and save the ODT file
    document = create_and_save_odt_file(file_path)

    # Insert text for 600 seconds
    if document:
        insert_text_for_duration(document, text_prefix, 600)

        # Close the document without saving further changes
        close_libreoffice_document(document, save_changes=False)
    else:
        print("Unable to open or create the document")


if __name__ == "__main__":
    libreoffice_uno()
