function Hero() {
  return (
    <section style={styles.hero}>
      <h1>Plataforma de Jogos Multiplayer</h1>

      <p>Descubra novos jogos, compita no ranking e desafie seus amigos.</p>

      <button style={styles.button}>Explorar Jogos</button>
    </section>
  );
}

const styles = {
  hero: {
    textAlign: "center",
    padding: "80px",
    background: "#222",
    color: "white"
  },
  button: {
    marginTop: "20px",
    padding: "12px 24px",
    fontSize: "16px"
  }
};

export default Hero;