package examplecode.eclipse;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

class CelestialBody {
    public double angle = 0;
    private final double angularVelocity;
    private final double orbitRadius;

    public CelestialBody(double angularVelocity, double orbitRadius) {
        this.angularVelocity = angularVelocity;
        this.orbitRadius = orbitRadius;
    }

    public void move() {
        angle += angularVelocity;
    }

    public double getX(double centerX) {
        System.out.println("angle: " + angle + " centerX: " + centerX + " orbitRadius: " + orbitRadius + " Math.cos(angle): " + Math.cos(angle));
        return centerX + orbitRadius * Math.cos(angle);
    }

    public double getY(double centerY) {
        return centerY + orbitRadius * Math.sin(angle);
    }
}

class SolarSystem extends JFrame {
    private static final int WIDTH = 800;
    private static final int HEIGHT = 800;

    private static final double EARTH_ORBIT_RADIUS = 200;
    private static final double MOON_ORBIT_RADIUS = 50;

    private static final double EARTH_ANGULAR_VELOCITY = 2 * Math.PI / 365; // 1 revolution per year
    private static final double MOON_ANGULAR_VELOCITY = 2 * Math.PI / 27; // 1 revolution per month

    private CelestialBody earth = new CelestialBody(EARTH_ANGULAR_VELOCITY, EARTH_ORBIT_RADIUS);
    private CelestialBody moon = new CelestialBody(MOON_ANGULAR_VELOCITY, MOON_ORBIT_RADIUS);

    public SolarSystem() {
        setSize(WIDTH, HEIGHT);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setVisible(true);

        Timer timer = new Timer(100, new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                earth.move();
                moon.move();
                repaint();
            }
        });
        timer.start();

        // Create a JPanel to hold the buttons and label
        JPanel panel = new JPanel();

        // Create the buttons and label
        JButton stopButton = new JButton("Stop");
        JButton pauseButton = new JButton("Pause");
        JButton forwardButton = new JButton("Forward");
        JButton backwardButton = new JButton("Backward");
        JLabel dayLabel = new JLabel("Day: 0");

        // Add action listeners to the buttons
        stopButton.addActionListener(e -> timer.stop());
        pauseButton.addActionListener(e -> {
            if (timer.isRunning()) {
                timer.stop();
            } else {
                timer.start();
            }
        });
        forwardButton.addActionListener(e -> {
            EARTH_ANGULAR_VELOCITY *= 2;
            MOON_ANGULAR_VELOCITY *= 2;
        });
        backwardButton.addActionListener(e -> {
            EARTH_ANGULAR_VELOCITY /= 2;
            MOON_ANGULAR_VELOCITY /= 2;
        });

        // Add the buttons and label to the panel
        panel.add(stopButton);
        panel.add(pauseButton);
        panel.add(forwardButton);
        panel.add(backwardButton);
        panel.add(dayLabel);

        // Add the panel to the frame
        add(panel, BorderLayout.SOUTH);

        // Update the day label in the timer's action listener
        timer.addActionListener(e -> {
            int day = (int) (earth.angle / EARTH_ANGULAR_VELOCITY);
            dayLabel.setText("Day: " + day);
        });
    }

    public void paint(Graphics g) {
        super.paint(g);
        int sunX = WIDTH / 2;
        int sunY = HEIGHT / 2;

        int earthX = (int) earth.getX(sunX);
        int earthY = (int) earth.getY(sunY);

        int moonX = (int) moon.getX(earthX);
        int moonY = (int) moon.getY(earthY);

        g.setColor(Color.YELLOW);
        g.fillOval(sunX - 50, sunY - 50, 100, 100);

        g.setColor(Color.BLUE);
        g.fillOval(earthX - 20, earthY - 20, 40, 40);

        g.setColor(Color.GRAY);
        g.fillOval(moonX - 10, moonY - 10, 20, 20);
    }

    public static void main(String[] args) {
        new SolarSystem();
    }

}