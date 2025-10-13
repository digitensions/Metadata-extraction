import json
import os
import sys
import csv
import subprocess
from datetime import datetime
from typing import Dict, Any, List, Final, Optional

# Example key database field names as key
MDATA_LIST: Final = [
    {"container_duration": ["Duration", "Duration  "]},
    {"container_file_size": ["FileSize", "File size  "]},
    {"container_format": ["Format", "Format  "]},
    {"container_audio_count": ["AudioCount", "Count of audio streams  "]},
    {"container_video_count": ["VideoCount", "Count of video streams  "]},
    {"container_format_profile": ["Format_Profile", "Format profile  "]},
    {"container_format_version": ["Format_Version", "Format version  "]},
    {"container_file_extension": ["FileExtension", "File extension  "]},
    {"video_duration": ["Duration", "Duration  "]},
    {"video_bit_depth": ["BitDepth", "Bit depth  "]},
    {"video_bit_rate_mode": ["BitRate_Mode", "Bit rate mode  "]},
    {"video_bit_rate": ["BitRate_String", "Bit rate  "]},
    {"video_chroma_subsampling": ["ChromaSubsampling", "Chroma subsampling"]},
    {"video_compression_mode": ["Compression_Mode", "Compression mode  "]},
    {"video_format_version": ["Format_Version", "Format version  "]},
    {"video_format_profile": ["Format_Profile", "Format profile  "]},
    {"video_format": ["Format", "Format  "]},
    {"video_frame_count": ["FrameCount", "Frame count  "]},
    {"video_frame_rate": ["FrameRate", "Frame rate  "]},
    {"video_height": ["Height", "Height  "]},
    {"video_width": ["Width", "Width  "]},
    {"video_scan_order": ["ScanOrder_String", "Scan order  "]},
    {"video_scan_type": ["ScanType", "Scan type  "]},
    {"video_codec": ["CodecID", "Codec ID  "]},
    {"video_dar": ["DisplayAspectRatio", "Display aspect ratio  "]},
    {"video_par": ["PixelAspectRatio", "Pixel aspect ratio  "]},
    {"video_colour_space": ["ColorSpace", "Color space  "]},
    {"video_colour_primaries": ["colour_primaries", "Color primaries  "]},
    {"video_matrix_coefficients": ["matrix_coefficients", "Matrix coefficients  "]},
    {"video_transfer_characteristics": ["transfer_characteristics", "Transfer characteristics  "]},
    {"audio_bit_depth": ["BitDepth", "Bit depth  "]},
    {"audio_bit_rate": ["BitRate_String", "Bit rate  "]},
    {"audio_bit_rate_mode": ["BitRate_Mode", "Bit rate mode  "]},
    {"audio_channels": ["Channels", "Channel(s)  "]},
    {"audio_codec": ["CodecID", "Codec ID  "]},
    {"audio_channel_layout": ["ChannelLayout", "Channel layout  "]},
    {"audio_channel_position": ["ChannelPositions", "Channel positions  "]},
    {"audio_compression_mode": ["Compression_Mode", "Compression mode  "]},
    {"audio_frame_count": ["FrameCount", "Frame count  "]},
    {"audio_stream_size": ["StreamSize_String", "Stream size  "]},
    {"audio_commercial_name": ["Format_Commercial", "Commercial name  "]},
    {"audio_format": ["Format", "Format  "]},
    {"audio_sampling_rate": ["SamplingRate_String", "Sampling rate  "]},
]

def get_file_mdata(fpath: str, type: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve mediainfo metadata
    with output set to type:
        JSON
    """
    with open(fpath, "r") as file:
        data = file.read()

    return json.loads(data)


def retrieve_metadata_dct(metadata: dict, stream: str, field: str) -> str:
    """
    Iterate received JSON metadata to match supplied
    field name, else return empty string.
    """
    media = metadata.get("media")

    return next(
        (
            track.get(field)
            for track in media.get("track")
            if track.get("@type") == stream
        ),
        "",
    )


def iterate_data_match(file_mdata: Dict[str, Any]) -> List[Any]:
    """
    Work through list extracting
    matching metadata
    """
    match_stream: Final = {
        "container": "General",
        "video": "Video",
        "audio": "Audio"
    }
    mdata_list = []
    for entry in MDATA_LIST:
        for k, v in entry.items():
            stream_type = k.split("_", 1)[0]
            stream = match_stream[stream_type]
            field = v[0]
            mdata = retrieve_metadata_dct(file_mdata, stream, field)
            mdata_list.append(mdata)

    return mdata_list


def write_to_csv(csv_path: str, filename: str, metadata: list) -> None:
    """
    Take list and write into CSV
    Create CSV first if not existing
    and create header row
    """
    metadata = [filename] + metadata

    if not os.path.isfile(csv_path):
        KEY_LIST = ["file_name"]
        with open(csv_path, "a+") as csvfile:
            for entry in MDATA_LIST:
                KEY_LIST.extend((iter(entry)))
            dataw = csv.writer(csvfile)
            dataw.writerow(KEY_LIST)

    with open(csv_path, "a") as csvfile:
        datawriter = csv.writer(csvfile)
        print(f"Adding to CSV :\n{metadata}")
        datawriter.writerow(metadata)


# The code that iterates and opens the files, matches metadata and writes it to CSV
print(os.listdir())
for root, _, files in os.walk("."):
    for file in files:
        if file.endswith((".py", ".csv")):
            continue
        fpath = os.path.join(root, file)
        mdata = get_file_mdata(fpath, "JSON")
        mdata_list = iterate_data_match(mdata)
        write_to_csv("metadata.csv", file, mdata_list)


with open("metadata.csv", "r") as file:
    csv_data = file.read()
    print("CSV contents:")
    print(csv_data)
