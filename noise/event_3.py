
import time
from pywpsrpc.rpcwpsapi import createWpsRpcInstance, wpsapi


def wps_write():
    time_init = time.time()
    state = True


    # Only create the RPC instance here.
    hr_word, rpc_word = createWpsRpcInstance()
    hr_word, app_word = rpc_word.getWpsApplication()
   
    #  Add a blank document.
    hr_word, doc = app_word.Documents.Add()
    time.sleep(1)

    # Add some text.
    selection = app_word.Selection
    while state:
        selection.InsertAfter("Hello, world")
        time.sleep(0.5)

        # Make the previously inserted 'Hello, world' bold.
        selection.Font.Bold = True

        # Move the cursor to the end.
        selection.EndKey()

        # Insert another empty paragraph.
        selection.InsertParagraph()

        # Move the cursor to the new paragraph.
        selection.MoveDown()

        # Type some more text.
        selection.TypeText("pywpsrpc~")
        time.sleep(0.5)

        # Move the cursor to the end.
        selection.EndKey()

        # Insert another empty paragraph.
        selection.InsertParagraph()

        # Move the cursor to the new paragraph.
        selection.MoveDown()

        if time.time() - time_init > 598:
            def onDocumentBeforeSave(doc):
                # If you want to cancel the saving of the current document, set the second return value to True.
                print("onDocumentBeforeSave called for doc: ", doc.Name)
                # SaveAsUI, Cancel
                return True, False

            # Register a notification before saving the document.
            rpc_word.registerEvent(app_word,
                                   wpsapi.DIID_ApplicationEvents4,
                                   "DocumentBeforeSave",
                                   onDocumentBeforeSave)

            # When saving the document, onDocumentBeforeSave will be called.
            doc.SaveAs2("./extra_data/office/test.docx")

            # Exit the WPS process.
            # Use wpsapi.wdDoNotSaveChanges to ignore document changes.
            doc.Close(SaveChanges=True)
            app_word.Quit()
            state = False

if __name__ == "__main__":
    wps_write()