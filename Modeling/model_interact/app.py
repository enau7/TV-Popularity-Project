from shiny import App, render, ui, run_app

import pandas as pd
import joblib

tv_df = pd.read_csv(r"C:\Users\Colton\Documents\GitHub\TV-Popularity-Project\Data\data\streaming_titles_clean.csv")

lm = joblib.load(r"C:\Users\Colton\Documents\GitHub\TV-Popularity-Project\Modeling\models\linear_regression.joblib")

genres = tv_df.columns[tv_df.columns.str.startswith('genre.')]
pretty_genre = lambda x: x[6:].replace("_"," ")

app_ui = ui.page_fluid(
    ui.input_select(id = "genre",
                    label = "Select a genre to be evaluated:",
                    choices = {item: pretty_genre(item) for item in genres.sort_values()}
                    ),
    ui.output_text_verbatim("txt"),
)


def server(input, output, session):
    @output
    @render.text
    def txt():
        model_input = tv_df.iloc[:0,:].copy()

        model_input.loc[0] = False
        try:
            model_input[input.genre()] = True
        except:
            return "An unexpected error occured."

        pred = lm.predict(model_input)[0]

        return f"{pretty_genre(input.genre())} titles are predicted to have a score of {round(pred,2)}."


app = App(app_ui, server)

if __name__ == "__main__":
    import os
    os.startfile("http://127.0.0.1:8000")
    run_app()
    exit()