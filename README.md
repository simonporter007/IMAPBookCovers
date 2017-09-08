# IMAPBookCovers

A KUAL extension to download books from a private email address using IMAP, direct to the Kindle and adding the book cover thumbnails. This allows emailing of formats not supported by Amazon "send to kindle" service and avoids the PDOC tag.

### Warning

This probably shouldn't be used out of the box without first seeing what it does. I have used this with a new email address that I will only send .azw3 books to myself.
The IMAP download does no validation other than downloading any attachment applied to an email from the last day and attempts to extract it using KindleUnpack.

If your use case does not fit this scenario, then you will need to modify the code yourself.

### Installing

1. Create a new directory on the kindle under `extensions` and call it `IMAPBookCovers`.
2. Clone or download the repo to your local machine and copy the contents to the new directory.

## Built With

* [KindleUnpack](https://github.com/kevinhendricks/KindleUnpack) - For extracting cover image
* [imaplib](https://docs.python.org/2/library/imaplib.html) - For IMAP email retrieval

## License

This project is licensed under the MIT License.

## Acknowledgments

* Thanks to BooksByMail for the inspiration.
