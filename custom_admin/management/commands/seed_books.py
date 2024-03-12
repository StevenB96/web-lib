from django.core.management.base import BaseCommand
import pandas as pd
from datetime import datetime
from custom_admin.model_classes import (
    Genre,
    Book,
    Author,
    BaseModel,
)


class Command(BaseCommand):
    def handle(self, *args, **options):
        book_data_A_path = "livi_datasets/book_data_A.csv"
        book_data_B_path = "livi_datasets/book_data_B.csv"

        # Read specific columns from the CSV file into a pandas DataFrame
        columns_to_read_A = [
            'original_title',
            'original_publication_year',
            'authors',
            'average_rating'
        ]
        book_df_A = pd.read_csv(book_data_A_path, usecols=columns_to_read_A)

        columns_to_read_B = [
            'title',
            'genre',
            'summary'
        ]
        book_df_B = pd.read_csv(book_data_B_path, usecols=columns_to_read_B)

        # Remove duplicates from both dataframes
        book_df_A.drop_duplicates(subset=['original_title'], inplace=True)
        book_df_B.drop_duplicates(subset=['title'], inplace=True)

        # Convert columns to lowercase for case-insensitive matching
        book_df_A['original_title_lc'] = book_df_A['original_title'].str.lower()
        book_df_B['title_lc'] = book_df_B['title'].str.lower()

        # Merge the DataFrames on the specified columns
        merged_df = pd.merge(
            book_df_A, 
            book_df_B, 
            left_on='original_title_lc', 
            right_on='title_lc', 
            how='inner'
        )

        # Remove rows with any empty values in any column
        book_df_A.dropna(inplace=True)
        book_df_B.dropna(inplace=True)

        for index, row in merged_df.iterrows():
            original_title = row['original_title']
            original_publication_year = row['original_publication_year']
            author = row['authors'].split(',')[0]
            average_rating = row['average_rating']
            title = row['title']
            genre = row['genre']
            summary = row['summary']

            genre_record, created = Genre.objects.get_or_create(
                name=genre,
                status=BaseModel.STATUS_CHOICES[1][0],
            )
            author_record, created = Author.objects.get_or_create(
                name=author,
                status=BaseModel.STATUS_CHOICES[1][0],
            )
            book_record, created = Book.objects.get_or_create(
                author=author_record,
                title=title,
                description=summary,
                rating=average_rating,
                published_date=self.convert_year_to_datetime(
                    original_publication_year),
                status=BaseModel.STATUS_CHOICES[1][0],
            )
            book_record.genres.add(genre_record)

    def convert_year_to_datetime(self, year):
        dt = datetime(int(year), 1, 1, 0, 0, 0)
        return dt.strftime('%Y-%m-%d %H:%M:%S')
