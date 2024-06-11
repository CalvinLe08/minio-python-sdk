# MinIO File Transfer Utility

## Overview

This Python script provides a command-line interface for uploading and downloading files to and from a MinIO server. It categorizes uploaded files into structured, semi-structured, and unstructured formats based on their extensions and saves downloaded files in specified directories with their original names.

## Features

- **Upload Files**: Automatically categorize and upload files to MinIO based on file extensions.
- **Download Files**: Download files from MinIO using the original file name and save them in a specified directory or the current directory by default.
- **Automatic Bucket Creation**: Automatically create the target bucket if it doesn't exist.

## Requirements

- Python 3.x
- Docker (to run the MinIO server using Docker Compose)
- MinIO Python SDK
