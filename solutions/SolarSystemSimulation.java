import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

// Encapsulation with private variables
public class SolarSystemSimulation extends JPanel implements ActionListener {
    private final int WIDTH = 800;
    private final int HEIGHT = 600;
    private final int EARTH_RADIUS = 20;
    private final int MOON_RADIUS = 5;
    private final int SUN_RADIUS = 50;
    private final int EARTH_ORBIT_RADIUS = 200;
    private final int MOON_ORBIT_RADIUS = 50;

    private double earthAngle = 0;
    private double moonAngle = 0;
    private boolean isRunning = false;
    private double dayCounter = 0;

    private final Timer timer = new Timer(1000, this); // increased the timer delay to 1 second

    private final JButton playButton = new JButton("Play");
    private final JButton pauseButton = new JButton("Pause");
    private final JButton stepButton = new JButton("Step");
    private final JLabel dayLabel = new JLabel("Day: 0");

    public SolarSystemSimulation() {
        setPreferredSize(new Dimension(WIDTH, HEIGHT));
        setLayout(new FlowLayout());
        setBackground(Color.BLACK); // Set the background color to black
        dayLabel.setForeground(Color.WHITE);

        playButton.addActionListener(e -> {
            isRunning = true;
            timer.start();
            step(); // start the simulation immediately
        });
        pauseButton.addActionListener(e -> {
            isRunning = false;
            timer.stop();
        });
        stepButton.addActionListener(e -> {
            step(); // added a call to the step method
        });

        add(playButton);
        add(pauseButton);
        add(stepButton);
        add(dayLabel);
    }

    @Override
    public void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2d = (Graphics2D) g;
        g2d.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);

        // Draw the sun
        g2d.setColor(Color.YELLOW);
        g2d.fillOval(WIDTH / 2 - SUN_RADIUS, HEIGHT / 2 - SUN_RADIUS, SUN_RADIUS * 2, SUN_RADIUS * 2);

        // Draw the Earth
        g2d.setColor(Color.BLUE);
        int earthX = WIDTH / 2 + (int) (Math.cos(earthAngle) * EARTH_ORBIT_RADIUS);
        int earthY = HEIGHT / 2 + (int) (Math.sin(earthAngle) * EARTH_ORBIT_RADIUS);
        g2d.fillOval(earthX - EARTH_RADIUS, earthY - EARTH_RADIUS, EARTH_RADIUS * 2, EARTH_RADIUS * 2);

        // Draw the Moon
        g2d.setColor(Color.GRAY);
        int moonX = earthX + (int) (Math.cos(moonAngle) * MOON_ORBIT_RADIUS);
        int moonY = earthY + (int) (Math.sin(moonAngle) * MOON_ORBIT_RADIUS);
        g2d.fillOval(moonX - MOON_RADIUS, moonY - MOON_RADIUS, MOON_RADIUS * 2, MOON_RADIUS * 2);
    }

    @Override
    public void actionPerformed(ActionEvent e) {
      if (isRunning) {
            step(); // advance the simulation by one day
            timer.setDelay(100); // set the timer delay to 100 milliseconds
        } else {
            timer.setDelay(0); // set the timer delay to 0 when not running
        }
    }

    private void step() {
        earthAngle += 0.01; // increment earth angle by a small amount (approx. 1 day)
        moonAngle += 0.05; // increment moon angle by a small amount (approx. 1 day)
        dayCounter += 0.5812; // increment day counter by 1 day
        dayLabel.setText("Day: " + (int) dayCounter); // update day label
        repaint(); // repaint the panel to update the positions
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame frame = new JFrame("Solar System Simulation");
            frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            frame.add(new SolarSystemSimulation());
            frame.pack();
            frame.setLocationRelativeTo(null);
            frame.setVisible(true);
        });
    }
}