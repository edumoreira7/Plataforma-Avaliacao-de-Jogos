function GameCard({ game }) {
  return (
    <div style={styles.card}>
      <img src={game.image} alt={game.name} style={styles.img} />

      <h3>{game.name}</h3>

      <p>⭐ {game.rating}</p>
      <p>👥 {game.players} jogadores</p>

      <button style={styles.button}>Ver jogo</button>
    </div>
  );
}

const styles = {
  card: {
    width: "235px",
    padding: "15px",
    borderRadius: "10px",
    background: "#1e1e1e",
    color: "white"
  },
  img: {
    width: "100%",
    borderRadius: "8px"
  },
  button: {
    marginTop: "10px",
    padding: "8px",
    width: "100%",
    cursor: "pointer"
  }
};

export default GameCard;