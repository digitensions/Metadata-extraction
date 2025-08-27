import json
import os
import sys

MDATA_LIST = [
    {"container.duration.seconds": ["Duration", "Duration  "]},
    {"container.file_size.total_bytes": ["FileSize", "File size  "]},
    {"container.commercial_name": ["Format_Commercial", "Commercial name  "]},
    {"container.format": ["Format", "Format  "]},
    {"container.audio_codecs": ["Audio_Codec_List", "Audio codecs "]},
    {"container.audio_stream_count": ["AudioCount", "Count of audio streams  "]},
    {"container.video_stream_count": ["VideoCount", "Count of video streams  "]},
    {"container.format_profile": ["Format_Profile", "Format profile  "]},
    {"container.format_version": ["Format_Version", "Format version  "]},
    {"container.encoded_date": ["Encoded_Date", "Encoded date  "]},
    {"container.frame_count": ["FrameCount", "Frame count  "]},
    {"container.frame_rate": ["FrameRate", "Frame rate  "]},
    {"container.overall_bit_rate": ["OverallBitRate_String", "Overall bit rate  "]},
    {"container.overall_bit_rate_mode": ["OverallBitRate_Mode", "Overall bit rate mode  ",]},
    {"container.writing_application": ["Encoded_Application", "Writing application  "]},
    {"container.writing_library": ["Encoded_Library", "Writing library  "]},
    {"container.file_extension": ["FileExtension", "File extension  "]},
    {"container.media_UUID": ["UniqueID", "Unique ID  "]},
    {"container.truncated": ["IsTruncated", "Is truncated  "]},
    {"video.duration.seconds": ["Duration", "Duration  "]},
    {"video.bit_depth": ["BitDepth", "Bit depth  "]},
    {"video.bit_rate_mode": ["BitRate_Mode", "Bit rate mode  "]},
    {"video.bit_rate": ["BitRate_String", "Bit rate  "]},
    {"video.chroma_subsampling": ["ChromaSubsampling", "Chroma subsampling"]},
    {"video.compression_mode": ["Compression_Mode", "Compression mode  "]},
    {"video.format_version": ["Format_Version", "Format version  "]},
    {"video.frame_count": ["FrameCount", "Frame count  "]},
    {"video.frame_rate": ["FrameRate", "Frame rate  "]},
    {"video.frame_rate_mode": ["FrameRate_Mode", "Frame rate mode  "]},
    {"video.height": ["Height", "Height  "]},
    {"video.scan_order": ["ScanOrder_String", "Scan order  "]},
    {"video.scan_type": ["ScanType", "Scan type  "]},
    {"video.scan_type.store_method": ["ScanType_StoreMethod_String", "Scan type, store method  "]},
    {"video.standard": ["Standard", "Standard  "]},
    {"video.stream_size_bytes": ["StreamSize", "Stream size  "]},
    {"video.stream_order": ["StreamOrder", "StreamOrder  "]},
    {"video.width": ["Width", "Width  "]},
    {"video.format_profile": ["Format_Profile", "Format profile  "]},
    {"video.width_aperture": ["Width_CleanAperture", "Width clean aperture  "]},
    {"video.delay": ["Delay", "Delay  "]},
    {"video.format_settings_GOP": ["Format_Settings_GOP", "Format settings, GOP  "]},
    {"video.codec_id": ["CodecID", "Codec ID  "]},
    {"video.colour_space": ["ColorSpace", "Color space  "]},
    {"video.colour_primaries": ["colour_primaries", "Color primaries  "]},
    {"video.commercial_name": ["Format_Commercial", "Commercial name  "]},
    {"video.display_aspect_ratio": ["DisplayAspectRatio", "Display aspect ratio  "]},
    {"video.format": ["Format", "Format  "]},
    {"video.matrix_coefficients": ["matrix_coefficients", "Matrix coefficients  "]},
    {"video.pixel_aspect_ratio": ["PixelAspectRatio", "Pixel aspect ratio  "]},
    {"video.transfer_characteristics": ["transfer_characteristics", "Transfer characteristics  "]},
    {"video.writing_library": ["Encoded_Library", "Writing library  "]},
    {"video.stream_size": ["StreamSize_String", "Stream size  "]},
    {"colour_range": ["colour_range", "Color range  "]},
    {"max_slice_count": ["MaxSlicesCount", "MaxSlicesCount  "]},
    {"audio.bit_depth": ["BitDepth", "Bit depth  "]},
    {"audio.bit_rate": ["BitRate_String", "Bit rate  "]},
    {"audio.bit_rate_mode": ["BitRate_Mode", "Bit rate mode  "]},
    {"audio.channels": ["Channels", "Channel(s)  "]},
    {"audio.codec_id": ["CodecID", "Codec ID  "]},
    {"audio.channel_layout": ["ChannelLayout", "Channel layout  "]},
    {"audio.channel_position": ["ChannelPositions", "Channel positions  "]},
    {"audio.compression_mode": ["Compression_Mode", "Compression mode  "]},
    {"audio.format_settings_endianness": ["Format_Settings_Endianness", "Format settings, Endianness  "]},
    {"audio.format_settings_sign": ["Format_Settings_Sign", "Format settings, Sign  "]},
    {"audio.frame_count": ["FrameCount", "Frame count  "]},
    {"audio.language": ["Language_String", "Language  "]},
    {"audio.stream_size_bytes": ["StreamSize", "Stream size  "]},
    {"audio.stream_order": ["StreamOrder", "StreamOrder  "]},
    {"audio.stream_size": ["StreamSize_String", "Stream size  "]},
    {"audio.commercial_name": ["Format_Commercial", "Commercial name  "]},
    {"audio.format": ["Format", "Format  "]},
    {"audio.sampling_rate": ["SamplingRate_String", "Sampling rate  "]},
]


def main():
    """
    receive file, and metadata type, output data
    """
    if not length(sys.argv) == 3:
        print("Please check you have supplied all required arguments:")
        print("python3 get_metadata.py <metadata> <CID field>")
        sys.exit()
    
    metadata_file = sys.argv[1]
    field_requested = sys.argv[2]
    for data in MDATA_LIST:
        if data.key() == field_requested:
            search = data.value()[num]

    if not os.path.exists(metadata_file):
        sys.exit(f"The path you have supplied cannot be found:\n{metadata_file}")
    
    if "json" in str(metadata_file).lower():
        with open(metadata_file) as file:
            metadata = json.load(file)
        m = retrieve_metadata_dct(metadata, search, 0)
        if m is None:
            sys.exit(f"No metadata found for {field_requested}. Sorry! Better luck next time.")
        print(f"Found metadata for {field_requested}: {m}")
        sys.exit(f"Please run the script again for more metadata... Good bye!")

    elif "text" in str(metadata_file).lower():
        with open(metadata_file) as file:
            metadata = readlines(file)
        m = retrieve_metadata_text(metadata, search, 1)
        if m is None:
            sys.exit(f"No metadata found for {field_requested}. Sorry! Better luck next time.")
        print(f"Found metadata for {field_requested}: {m}")
        sys.exit(f"Please run the script again for more metadata... Good bye!")

    else:
        sys.exit("Could not determine metadata supply type. Please try again with a better source.")
    

def retrieve_metadata_dct(metadata, field, num):
    """
    Iterate MDATA_LIST to match supplied
    field name if possible.
    """
    media = metadata.get("media")
    for track in media.get("track"):
        for k, v in track.items():
            if k == search:
            return f"{track.get("@type")} {v}")

    return None


def retrieve_metadata_text(metadata, field, num):
    """
    Split string, then read lines to match
    field name where possible.
    """
    lines = metadata.split("\n")
    if not len(lines) > 2:
        return None
    for line in lines:
        if line.startswith(field):
            field_entry = row.split(":", 1)[-1].strip()
            return field_entry


if __name__ == "__main__":
    main()
