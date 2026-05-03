import streamlit as st

from dropshipping_game.game import DropshippingGame


game: DropshippingGame = DropshippingGame()


def main() -> None:
    st.title("Dropshipping Game Draft")
    st.write("TODO: build the Streamlit UI here.")
    st.json(game.__dict__)


if __name__ == "__main__":
    main()
