import os
import shutil
import sys
import click

categories = {
    'images': ['jpeg', 'png', 'jpg', 'svg'],
    'videos': ['avi', 'mp4', 'mov', 'mkv'],
    'documents': ['doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx'],
    'audio': ['mp3', 'ogg', 'wav', 'amr'],
    'archives': ['zip', 'gz', 'tar']
}

categorized_files = {category: [] for category in categories}


def get_info_about_folder(folder):
    all_extensions = set()
    unknown_extensions = set()

    # Traverse through the folder and its subfolders recursively
    for root, dirs, files in os.walk(folder):
        for file in files:
            # Get the file extension
            extension = os.path.splitext(file)[1][1:]
            all_extensions.add(extension)

            # Categorize the file based on its extension
            categorized = False
            for category, extensions in categories.items():
                if extension in extensions:
                    categorized_files[category].append(os.path.join(root, file))
                    categorized = True
                    break

            # If the extension is not recognized, add it to the unknown extensions set
            if not categorized:
                unknown_extensions.add(extension)

    # Print the results
    print("Categorized files:")
    for category, files in categorized_files.items():
        print(f"{category}: {len(files)} files")
        for file in files:
            print(f"\t{file}")
    print()

    print("All extensions found:")
    for extension in sorted(all_extensions):
        print(extension)
    print()

    if len(unknown_extensions) > 0:
        print("Unknown extensions found:")
        for extension in sorted(unknown_extensions):
            print(extension)
    print()


def delete_empty_folders(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for dir_n in dirs:
            if dir_n not in categories.keys():
                dir_path = os.path.join(root, dir_n)
                if not os.listdir(dir_path):
                    try:
                        os.rmdir(dir_path)
                    except Exception as e:
                        print(f"Error deleting folder {dir_path}: {e}")


def rename(path):
    # Rename all files and folders recursively in the given directory
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files + dirs:
            old_path = os.path.join(root, name)
            name_without_ext, ext = os.path.splitext(name)
            new_name_without_ext = normalize(name_without_ext)
            new_name = new_name_without_ext + ext
            new_path = os.path.join(root, new_name)
            try:
                os.rename(old_path, new_path)
            except PermissionError:
                print("\nAn error occurred while renaming files."
                      "\nTarget files or folders are used by other programs."
                      "\nPlease close these programs and try again.")
                return


def normalize(text):
    # define dictionary for transliteration
    translit_dict = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
        'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
        'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
        'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
        'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch',
        'ш': 'sh', 'щ': 'shch', 'ъ': '', 'ы': 'y', 'ь': '',
        'э': 'e', 'є': 'e', 'ю': 'yu', 'я': 'ya',
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D',
        'Е': 'E', 'Ё': 'Yo', 'Ж': 'Zh', 'З': 'Z', 'И': 'I',
        'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N',
        'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T',
        'У': 'U', 'Ф': 'F', 'Х': 'Kh', 'Ц': 'Ts', 'Ч': 'Ch',
        'Ш': 'Sh', 'Щ': 'Shch', 'Ъ': '', 'Ы': 'Y', 'Ь': '',
        'Э': 'E', 'Є': 'E', 'Ю': 'Yu', 'Я': 'Ya'
    }
    # transliterate the text
    translit_text = ''
    for char in text:
        if char.isalpha() and char in translit_dict:
            translit_text += translit_dict[char]
        elif char.isdigit() or char.isalpha():
            translit_text += char
        else:
            translit_text += '_'
    return translit_text


def transfer_images(path):
    # Create the images folder if it doesn't exist
    os.makedirs(os.path.join(path, 'images'), exist_ok=True)

    # Transfer the images to the images folder
    for image_path in categorized_files['images']:
        image_name = os.path.basename(image_path)
        shutil.move(image_path, os.path.join(path, 'images', image_name))


def transfer_videos(path):
    # Create the videos folder if it doesn't exist
    os.makedirs(os.path.join(path, 'videos'), exist_ok=True)

    # Transfer the videos to the videos folder
    for video_path in categorized_files['videos']:
        video_name = os.path.basename(video_path)
        shutil.move(video_path, os.path.join(path, 'videos', video_name))


def transfer_documents(path):
    # Create the documents folder if it doesn't exist
    os.makedirs(os.path.join(path, 'documents'), exist_ok=True)

    # Transfer the documents to the documents folder
    for document_path in categorized_files['documents']:
        document_name = os.path.basename(document_path)
        shutil.move(document_path, os.path.join(path, 'documents', document_name))


def transfer_audio(path):
    # Create the audio folder if it doesn't exist
    os.makedirs(os.path.join(path, 'audio'), exist_ok=True)

    # Transfer the audio files to the audio folder
    for audio_path in categorized_files['audio']:
        audio_name = os.path.basename(audio_path)
        shutil.move(audio_path, os.path.join(path, 'audio', audio_name))


def extract_archives(path):
    archives_folder = os.path.join(path, 'archives')
    os.makedirs(archives_folder, exist_ok=True)
    for file_path in categorized_files['archives']:
        file_name = os.path.basename(file_path)
        file_name_no_ext = os.path.splitext(file_name)[0]
        destination_folder = os.path.join(archives_folder, file_name_no_ext)
        os.makedirs(destination_folder, exist_ok=True)
        shutil.unpack_archive(file_path, destination_folder)
        os.remove(file_path)


def sort(path):
    transfer_videos(path)
    transfer_images(path)
    transfer_documents(path)
    transfer_audio(path)
    extract_archives(path)



@click.command()
@click.argument('folder')
def main(folder):
    try:
        rename(folder)

        get_info_about_folder(folder)

        sort(folder)

        delete_empty_folders(folder)

    except:
        print('\nAn error occurred. In order for the script to work correctly, close the target folder and try again.')


if __name__ == '__main__':
    main()