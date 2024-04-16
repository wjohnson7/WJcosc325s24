import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.util.ArrayList;
import java.util.List;

public class OrbitSimulation extends JFrame {
    private final int width = 800;
    private final int height = 800;
    private DrawingPanel drawingPanel;
    private Timer timer;
    private JButton playButton, pauseButton, stepButton;
    private JLabel dayLabel;
    private int days = 0;

    public OrbitSimulation() {
        setTitle("Orbit Simulation");
        setSize(width, height);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLayout(new BorderLayout());

        drawingPanel = new DrawingPanel();
        add(drawingPanel, BorderLayout.CENTER);

        JPanel controlPanel = new JPanel();
        playButton = new JButton("Play");
        pauseButton = new JButton("Pause");
        stepButton = new JButton("Step");
        dayLabel = new JLabel("Day: " + days);

        controlPanel.add(playButton);
        controlPanel.add(pauseButton);
        controlPanel.add(stepButton);
        controlPanel.add(dayLabel);

        add(controlPanel, BorderLayout.SOUTH);

        setupActions();
        timer = new Timer(100, e -> stepSimulation());
        pack();
    }

    private void setupActions() {
        playButton.addActionListener(e -> timer.start());
        pauseButton.addActionListener(e -> timer.stop());
        stepButton.addActionListener(e -> stepSimulation());
    }

    private void stepSimulation() {
        days++;
        dayLabel.setText("Day: " + days);
        drawingPanel.move();
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new OrbitSimulation().setVisible(true));
    }

    class DrawingPanel extends JPanel {
        List<CelestialBody> bodies = new ArrayList<>();

        public DrawingPanel() {
            setPreferredSize(new Dimension(width, height));
            setBackground(Color.BLACK);
            initializeOrbits();
        }

        private void initializeOrbits() {
            CelestialBody sun = new CelestialBody("Sun", 20, Color.YELLOW, null, 0, 0);
            CelestialBody earth = new CelestialBody("Earth", 10, Color.BLUE, sun, 250, 2 * Math.PI / 365.256);
            CelestialBody moon = new CelestialBody("Moon", 5, Color.GRAY, earth, 20, 2 * Math.PI / 27.3);
            bodies.add(sun);
            bodies.add(earth);
            bodies.add(moon);
        }

        public void move() {
            for (CelestialBody body : bodies) {
                body.updatePosition();
            }
            repaint();
        }

        @Override
        protected void paintComponent(Graphics g) {
            super.paintComponent(g);
            for (CelestialBody body : bodies) {
                body.draw(g, getWidth() / 2, getHeight() / 2);
            }
        }
    }

    class CelestialBody {
        String name;
        int size;
        Color color;
        CelestialBody orbitCenter;
        double radius;
        double angle;
        double speed;

        public CelestialBody(String name, int size, Color color, CelestialBody orbitCenter, double radius, double speed) {
            this.name = name;
            this.size = size;
            this.color = color;
            this.orbitCenter = orbitCenter;
            this.radius = radius;
            this.angle = 0;
            this.speed = speed;
        }

        void updatePosition() {
            if (orbitCenter != null) {
                angle += speed;
            }
        }

        void draw(Graphics g, int offsetX, int offsetY) {
            int x = (int) (offsetX + (orbitCenter != null ? orbitCenter.getX() : 0) + radius * Math.cos(angle));
            int y = (int) (offsetY + (orbitCenter != null ? orbitCenter.getY() : 0) + radius * Math.sin(angle));
            g.setColor(color);
            g.fillOval(x - size / 2, y - size / 2, size, size);
        }

        int getX() {
            return (int) (orbitCenter != null ? orbitCenter.getX() + radius * Math.cos(angle) : 0);
        }

        int getY() {
            return (int) (orbitCenter != null ? orbitCenter.getY() + radius * Math.sin(angle) : 0);
        }
    }
}
