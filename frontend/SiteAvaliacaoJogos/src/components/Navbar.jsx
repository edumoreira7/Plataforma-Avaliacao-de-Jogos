function Navbar() {
  return (
    <nav style={styles.nav}>
      <h2>GameHub</h2>

      <div>
        <button style={styles.btn}>Login</button>
        <button style={styles.btn}>Cadastrar</button>
      </div>
    </nav>
  );
}

const styles = {
  nav: {
    display: "flex",
    justifyContent: "space-between",
    padding: "20px",
    background: "#111",
    color: "white"
  },
  btn: {
    marginLeft: "10px",
    padding: "8px 16px",
    cursor: "pointer"
  }
};

export default Navbar;