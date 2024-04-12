package examplecode.eclipse;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class Main extends JFrame {
    private static final int WIDTH = 800;
    private static final int HEIGHT = 800;

    private static final double EARTH_ORBIT_RADIUS = 200;
    private static final double MOON_ORBIT_RADIUS = 50;

    private static final double EARTH_ANGULAR_VELOCITY = 2 * Math.PI / 365; // 1 revolution per year
    private static final double MOON_ANGULAR_VELOCITY = 2 * Math.PI / 27; // 1 revolution per month

    private double earthAngle = 0;
    private double moonAngle = 0;

    public Main() {
        setSize(WIDTH, HEIGHT);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setVisible(true);

        Timer timer = new Timer(100, new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                earthAngle += EARTH_ANGULAR_VELOCITY;
                moonAngle += MOON_ANGULAR_VELOCITY;
                repaint();
            }
        });
        timer.start();
    }

    public void paint(Graphics g) {
        super.paint(g);
        int sunX = WIDTH / 2;
        int sunY = HEIGHT / 2;

        int earthX = sunX + (int) (EARTH_ORBIT_RADIUS * Math.cos(earthAngle));
        int earthY = sunY + (int) (EARTH_ORBIT_RADIUS * Math.sin(earthAngle));

        int moonX = earthX + (int) (MOON_ORBIT_RADIUS * Math.cos(moonAngle));
        int moonY = earthY + (int) (MOON_ORBIT_RADIUS * Math.sin(moonAngle));

        g.setColor(Color.YELLOW);
        g.fillOval(sunX - 50, sunY - 50, 100, 100);

        g.setColor(Color.BLUE);
        g.fillOval(earthX - 20, earthY - 20, 40, 40);

        g.setColor(Color.GRAY);
        g.fillOval(moonX - 10, moonY - 10, 20, 20);
    }

    public static void main(String[] args) {
        new Main();
    }
}
