# NewsMailer

**NewsMailer** automates the process of fetching the latest newspapers from online sources and delivering them straight to your inbox.

## Why NewsMailer?

Enjoy your morning coffee or afternoon break while staying updated with the latest news! With **NewsMailer**, you can schedule news delivery at your preferred time, whether in the morning or afternoon, and receive the latest articles right in your inbox. No need to manually browse news sites—just sit back, relax, and let the news come to you!

## Features

- **Automated News Retrieval:** Fetches the latest news articles from news websites.
- **Email Delivery:** Sends the fetched articles directly to specified email addresses.
- **Scheduled Delivery:** Set up your preferred time to receive the news, whether it's in the morning or afternoon.
- **Docker Support:** Easily deployable using Docker.
- **Environment Configuration:** Configure your environment variables easily with a setup script.

## Configuration

**Docker Arguments:**

- `DAWN_SCRAPER_BASE_URL`: The base URL for the DAWN news site to scrape.
- `DAWN_SCRAPER_SECTIONS_TO_RETRIEVE`: Specific sections of DAWN news to retrieve (e.g., world, sports).
- `MAIL_API_KEY`: API key for the email service used to send the news.
- `MAIL_SENDER`: The email address that will appear as the sender.
- `MAIL_RECIPIENTS`: Comma-separated list of email addresses that will receive the news.
- `STORAGE_ENDPOINT`: The endpoint for the cloud storage service where files will be saved.
- `STORAGE_ACCESS_KEY`: Access key for the cloud storage service.
- `STORAGE_SECRET_KEY`: Secret key for the cloud storage service.
- `STORAGE_BUCKET`: Name of the storage bucket where files will be uploaded.
- `STORAGE_PATH_PREFIX`: Path prefix in the storage bucket for organizing files.
- `GMT`: Timezone in GMT for scheduling the news retrieval.
- `IMAGE_QUALITY`: Quality setting for images to be included in the emails.
- `CRON_HOUR`: Hour in GMT to schedule the news retrieval.
- `CRON_MINUTE`: Minute in GMT to schedule the news retrieval.

## Installation

To get started with NewsMailer, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/devs-talha/news-mailer.git
   cd news-mailer
   ```

2. **Build Docker image:**

   Build the Docker image:

   ```bash
   docker build \
    --build-arg DAWN_SCRAPER_BASE_URL="https://www.dawn.com" \
    --build-arg DAWN_SCRAPER_SECTIONS_TO_RETRIEVE="world,sports" \
    --build-arg MAIL_API_KEY="your-mail-api-key" \
    --build-arg MAIL_SENDER="sender@example.com" \
    --build-arg MAIL_RECIPIENTS="recipient1@example.com,recipient2@example.com" \
    --build-arg STORAGE_ENDPOINT="https://storage.example.com" \
    --build-arg STORAGE_ACCESS_KEY="your-storage-access-key" \
    --build-arg STORAGE_SECRET_KEY="your-storage-secret-key" \
    --build-arg STORAGE_BUCKET="news-bucket" \
    --build-arg STORAGE_PATH_PREFIX="news" \
    --build-arg GMT="0" \
    --build-arg IMAGE_QUALITY="high" \
    --build-arg CRON_HOUR="7" \
    --build-arg CRON_MINUTE="30" \
    -t newsmailer .
   ```

3. **Run the application:**

   ```bash
   docker run -d newsmailer
   ```

## Supported News Sources

- **DAWN News**: Currently, the application supports fetching articles from DAWN news.

## Contributing

If you'd like to contribute to this project, feel free to open a pull request or report any issues you find. Contributions are welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
