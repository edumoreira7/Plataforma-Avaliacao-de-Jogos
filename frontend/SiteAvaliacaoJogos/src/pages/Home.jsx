import Navbar from "../components/Navbar";
import Hero from "../components/Hero";
import GameList from "../components/GameList";
import Leaderboard from "../components/Leaderboard";

import { games } from "../data/games";

function Home() {
  return (
    <>
      <Navbar />
      <Hero />
      <GameList games={games} />
      <Leaderboard />
    </>
  );
}

export default Home;