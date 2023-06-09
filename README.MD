# School downloader

This is a quick and ugly project to download schools from the NCES website.  It is not intended to be used by anyone else, but feel free to use it if you want.  Ask me if you have any questions.

## Description

This project downloads schools from the [National Center for
Education Statistics](https://nces.ed.gov/ccd/schoolsearch/) website.

It scapes the pages by zip code, using  zip codes from [USP zip codes CSV](https://postalpro.usps.com/ZIP_Locale_Detail).

## school_downloader.py

This script downloads the schools from the NCES website and saves the html files in the `saved_pages` folder.

## convert_to_csv.py

This scrip converts the html files to csv files and saves them in the `results` folder.

## watch.sh

Monitors the progress of the download.  It will print the number of files in the `saved_pages` folder every 10 seconds.  It will send an e-mail when the process is completes or crashes.

This works on my Mac, but I'm not sure if it will work on other systems.  Posfix is required to send the e-mail.

## Background

While on vacation, my niece asked if I could help her generate a list of schools in the US for a non profit that she runs.  I'm also looking for better approaches to leveraging ChatGPT and Copilot, so I thought this would be a good project to try.
