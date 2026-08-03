package co.edu.unab.practica.db;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public final class ConexionFactory {
    private final String url;
    private final String usuario;
    private final String password;

    public ConexionFactory(String url, String usuario, String password) {
        if (url == null || url.isBlank()) {
            throw new IllegalArgumentException("DB_URL es obligatoria");
        }
        if (usuario == null || usuario.isBlank()) {
            throw new IllegalArgumentException("DB_USER es obligatorio");
        }
        if (password == null) {
            throw new IllegalArgumentException("DB_PASSWORD es obligatoria");
        }
        this.url = url;
        this.usuario = usuario;
        this.password = password;
    }

    public static ConexionFactory desdeEntorno() {
        return new ConexionFactory(
                System.getenv("DB_URL"),
                System.getenv("DB_USER"),
                System.getenv("DB_PASSWORD"));
    }

    public Connection abrir() throws SQLException {
        return DriverManager.getConnection(url, usuario, password);
    }
}
