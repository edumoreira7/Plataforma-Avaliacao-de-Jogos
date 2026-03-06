import GameCard from "./GameCard";

function GameList({ games }) {
  return (
    <section style={styles.container}>
      <h2>Jogos em destaque</h2>

      <div style={styles.grid}>
        {games.map((game) => (
          <GameCard key={game.id} game={game} />
        ))}
      </div>
    </section>
  );
}

const styles = {
  container: {
    padding: "40px"
  },
  grid: {
    display: "flex",
    gap: "20px",
    flexWrap: "wrap"
  }
};

export default GameList;