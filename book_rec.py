# import
import pandas as pd
import numpy as np


def rec(dataset, dataset_lowercase, title_orig):
    title = title_orig.lower()

    author = dataset_lowercase.loc[dataset_lowercase['Book-Title'] == title, 'Book-Author'].values[0]

    book_readers = dataset_lowercase['User-ID'][(dataset_lowercase['Book-Title']==title) & (dataset_lowercase['Book-Author'].str.contains(author))]
    book_readers = book_readers.tolist()
    book_readers = np.unique(book_readers)

    # final dataset
    books_of_book_readers = dataset_lowercase[(dataset_lowercase['User-ID'].isin(book_readers))]
    # Number of ratings per other books in dataset
    number_of_rating_per_book = books_of_book_readers.groupby(['Book-Title']).agg('count').reset_index()

    #select only books which have actually higher number of ratings than threshold
    books_to_compare = number_of_rating_per_book['Book-Title'][number_of_rating_per_book['User-ID'] >= 8]
    books_to_compare = books_to_compare.tolist()

    ratings_data_raw = books_of_book_readers[['User-ID', 'Book-Rating', 'Book-Title', 'Image-URL-M', 'Book-Author']][books_of_book_readers['Book-Title'].isin(books_to_compare)]


    # group by User and Book and compute mean
    ratings_data_raw_nodup = ratings_data_raw.groupby(['User-ID', 'Book-Title'])['Book-Rating'].mean()

    # reset index to see User-ID in every row
    ratings_data_raw_nodup = ratings_data_raw_nodup.to_frame().reset_index()

    dataset_for_corr = ratings_data_raw_nodup.pivot(index='User-ID', columns='Book-Title', values='Book-Rating')

    Book_list= [title]

    result_list = []
    worst_list = []

    # for each of the trilogy book compute:
    for Reader_book in Book_list:

        #Take out the Lord of the Rings selected book from correlation dataframe
        dataset_of_other_books = dataset_for_corr.copy(deep=False)
        dataset_of_other_books.drop([Reader_book], axis=1, inplace=True)


        # empty lists
        book_titles = []
        correlations = []
        avgrating = []
        img = []
        authors = []

        # corr computation
        for book_title in list(dataset_of_other_books.columns.values):
            book_titles.append(book_title)
            img.append(dataset.loc[dataset_lowercase['Book-Title']== book_title, 'Image-URL-M'].values[0])
            authors.append(dataset.loc[dataset_lowercase['Book-Title']== book_title, 'Book-Author'].values[0])
            correlations.append(dataset_for_corr[Reader_book].corr(dataset_of_other_books[book_title]))
            tab=(ratings_data_raw[ratings_data_raw['Book-Title']==book_title].groupby(ratings_data_raw['Book-Title']).mean())
            avgrating.append(tab['Book-Rating'].min())
        # final dataframe of all correlation of each book
        corr_fellowship = pd.DataFrame(list(zip(book_titles, correlations, avgrating, img, authors)), columns=['book','corr','avg_rating', 'img', 'author'])
        corr_fellowship.head()



        # top 10 books with highest corr
        result_list.append(corr_fellowship.sort_values('corr', ascending = False).head(10))

        #worst 10 books
        worst_list.append(corr_fellowship.sort_values('corr', ascending = False).tail(10))
    return result_list[0].to_dict()

