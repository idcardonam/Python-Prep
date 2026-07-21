package co.edu.unab.web;

import jakarta.servlet.Filter;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.ServletRequest;
import jakarta.servlet.ServletResponse;
import jakarta.servlet.annotation.WebFilter;
import jakarta.servlet.http.HttpServletResponse;

import java.io.IOException;
import java.nio.charset.StandardCharsets;

@WebFilter("/*")
public final class Utf8SecurityHeadersFilter implements Filter {

    @Override
    public void doFilter(
            ServletRequest request,
            ServletResponse response,
            FilterChain chain) throws IOException, ServletException {
        request.setCharacterEncoding(StandardCharsets.UTF_8.name());
        response.setCharacterEncoding(StandardCharsets.UTF_8.name());

        if (response instanceof HttpServletResponse http) {
            http.setHeader("X-Content-Type-Options", "nosniff");
            http.setHeader("X-Frame-Options", "DENY");
            http.setHeader(
                    "Content-Security-Policy",
                    "default-src 'self'; style-src 'self' 'unsafe-inline'");
        }

        chain.doFilter(request, response);
    }
}
