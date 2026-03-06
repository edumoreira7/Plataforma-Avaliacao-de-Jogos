const players = [
  { name: "PlayerOne", score: 1500 },
  { name: "DarkGamer", score: 1300 },
  { name: "NeoPlayer", score: 1100 }
];

function Leaderboard() {
  return (
    <section style={{ padding: "40px" }}>
      <h2>Top Jogadores</h2>

      <ol>
        {players.map((p, i) => (
          <li key={i}>
            {p.name} — {p.score} pts
          </li>
        ))}
      </ol>
    </section>
  );
}

export default Leaderboard;