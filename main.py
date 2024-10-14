# MIT License
#
# Copyright (c) 2024 Sariya Ansari
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


"""
Main Test File

This script contains test functions for various operations related to AES encryption,
HLS conversion, and WebVTT generation. It utilizes the CryptoManager for handling encryption
and decryption, and Scrubber for thumbnail and WebVTT generation.

Author: [Your Name]
"""

import os
from thumbtrail.cryptomanager import CryptoManager
from thumbtrail.scrubber import Scrubber


def crypto_aes_test():
    """
    Test AES encryption and decryption for video files.

    The function demonstrates how to generate AES keys, encrypt a video, and decrypt it using `CryptoManager`.
    """
    crypto_manager = CryptoManager()

    input_video = 'samples/sample_file.mp4'
    encrypted_video = 'output/aes/encrypted_video.mp4'
    decrypted_video = 'output/aes/decrypted_video.mp4'
    key_file = 'output/aes/aes_key.key'
    iv_file = 'output/aes/aes_iv.key'

    # Generate AES key and IV
    crypto_manager.generate_aes_key_iv()

    # Optionally, save the generated key and IV to files for later use
    crypto_manager.save_aes_key_iv(key_file, iv_file)

    # Encrypt the video
    crypto_manager.encrypt_video_aes(input_video, encrypted_video)

    # Decrypt the video
    crypto_manager.decrypt_video_aes(encrypted_video, decrypted_video)

    # Alternatively, load the AES key and IV from files for decryption
    crypto_manager.load_aes_key_iv(key_file, iv_file)
    crypto_manager.decrypt_video_aes(encrypted_video, decrypted_video)


def convert_to_hls_test():
    """
    Test converting a video to HLS format without encryption.

    This function demonstrates how to use `CryptoManager` to convert a video to an HLS stream without encryption.
    """
    crypto_manager = CryptoManager()
    input_video = 'samples/sample_file.mp4'
    output_dir = 'output/test1'

    crypto_manager.convert_video_to_hls(input_video, output_dir)


def convert_to_encrypted_hls_test():
    """
    Test converting a video to HLS format with encryption.

    This function demonstrates how to use `CryptoManager` to generate HLS key info and convert a video to an encrypted HLS stream.
    """
    crypto_manager = CryptoManager()
    input_video = 'samples/sample_file.mp4'
    output_dir = 'output/test2'

    key_file, key_info_file, iv_hex = crypto_manager.generate_hls_key_info(output_dir)
    crypto_manager.convert_video_to_hls(input_video, output_dir, key_info_file)


def encrypt_existing_hls_test():
    """
    Test encrypting an existing clear HLS stream.

    This function demonstrates how to encrypt an existing clear HLS stream using `CryptoManager`.
    """
    crypto_manager = CryptoManager()
    playlist_file = 'output/test1/output.m3u8'
    output_dir = 'output/test3'

    crypto_manager.encrypt_existing_hls(playlist_file, output_dir)


def decrypt_hls_test():
    """
    Test decrypting an encrypted HLS stream.

    This function checks whether the HLS stream is encrypted and proceeds to decrypt it using `CryptoManager`.
    It verifies if an AES key and optionally an IV are available for decryption.
    """
    crypto_manager = CryptoManager()
    playlist_file = 'output/test2/output.m3u8'
    decryption_key_file = 'output/test2/hls_key.key'
    iv_file = 'output/test2/hls_iv.key'
    decrypted_output_file = 'output/test4/output_decrypted.mp4'

    output_dir = os.path.dirname(decrypted_output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if os.path.exists(decryption_key_file):
        print("Encrypted stream detected. Proceeding with decryption...")

        with open(decryption_key_file, 'rb') as f:
            decryption_key = f.read()

        decryption_key_hex = decryption_key.hex()

        if os.path.exists(iv_file):
            print("IV detected. Proceeding with IV...")
            with open(iv_file, 'rb') as f:
                iv_hex = f.read().hex()
            crypto_manager.decrypt_hls_video(playlist_file, decrypted_output_file, decryption_key_hex, iv_hex)
        else:
            crypto_manager.decrypt_hls_video(playlist_file, decrypted_output_file, decryption_key_hex)
    else:
        print("No encryption detected. Skipping decryption.")


def webvtt_clear_stream_test():
    """
    Test generating WebVTT and thumbnails for a clear video stream.

    This function demonstrates how to use `Scrubber` to generate thumbnails and WebVTT files for a clear video stream.
    """
    video_path = "output/aes/decrypted_video.mp4"
    output_dir = "output/webvtt_clear"

    thumb_scrub = Scrubber(video_path, output_dir)

    thumb_scrub.generate_thumbnails_and_webvtt(
        interval=2,
        thumbnail_size=(160, 90),
        image_format="jpg",
        should_merge_thumbnails=True,
        use_absolute_paths=False
    )
    print("Test for clear stream completed successfully.")


def webvtt_encrypted_aes_test():
    """
    Test generating WebVTT and thumbnails for an AES-encrypted video stream.

    This function demonstrates how to use `Scrubber` to decrypt an AES-encrypted video and generate thumbnails and WebVTT files.
    """
    video_path = "output/aes/encrypted_video.mp4"
    output_dir = "output/webvtt_aes"
    key_file = "output/aes/aes_key.key"
    iv_file = "output/aes/aes_iv.key"

    thumb_scrub = Scrubber(
        video_path, output_dir,
        decryption_method='AES',
        key_file=key_file,
        iv_file=iv_file
    )

    thumb_scrub.generate_thumbnails_and_webvtt(
        interval=2,
        thumbnail_size=(160, 90),
        image_format="jpg",
        should_merge_thumbnails=False,
        use_absolute_paths=False
    )
    print("Test for AES-encrypted stream completed successfully.")


def webvtt_encrypted_hls_test():
    """
    Test generating WebVTT and thumbnails for an HLS-encrypted video stream.

    This function demonstrates how to use `Scrubber` to decrypt an HLS-encrypted video and generate thumbnails and WebVTT files.
    """
    video_path = "output/test2/output.m3u8"
    output_dir = "output/webvtt_hls"
    key_file = "output/test2/hls_key.key"
    iv_file = "output/test2/hls_key_info.txt"

    thumb_scrub = Scrubber(
        video_path, output_dir,
        decryption_method='HLS',
        key_file=key_file
    )

    thumb_scrub.generate_thumbnails_and_webvtt(
        interval=2,
        thumbnail_size=(160, 90),
        image_format="jpg",
        should_merge_thumbnails=False,
        use_absolute_paths=True,
        thumbnail_url="http://www.myscrubber.com"
    )
    print("Test for HLS-encrypted stream completed successfully.")


if __name__ == '__main__':
    crypto_aes_test()
    convert_to_hls_test()
    convert_to_encrypted_hls_test()
    encrypt_existing_hls_test()
    decrypt_hls_test()

    webvtt_clear_stream_test()
    webvtt_encrypted_aes_test()
    webvtt_encrypted_hls_test()
