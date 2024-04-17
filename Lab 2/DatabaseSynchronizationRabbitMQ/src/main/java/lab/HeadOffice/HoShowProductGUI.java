package lab.HeadOffice;

import lab.*;

import javax.swing.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.Color;
import javax.swing.border.EmptyBorder;
import java.awt.GridLayout;
import java.awt.BorderLayout;

public class HoShowProductGUI {

    public HoShowProductGUI(String dbName) {
        JFrame f = new JFrame(dbName);
        f.setSize(600, 400); // Adjusted size for better display
        JPanel p = new JPanel();
        p.setBorder(new EmptyBorder(10, 10, 10, 10));
        p.setBackground(new Color(216, 191, 216));
        p.setLayout(new GridLayout(7, 2, 15, 10)); // Adjusted grid layout
        f.add(p, BorderLayout.CENTER);
        JLabel nameLabel = new JLabel("Name:");
        p.add(nameLabel);
        JTextField t1 = new JTextField(20);
        p.add(t1);
        JLabel priceLabel = new JLabel("Price:");
        p.add(priceLabel);
        JTextField t2 = new JTextField(20);
        p.add(t2);
        JLabel descriptionLabel = new JLabel("Description:");
        p.add(descriptionLabel);
        JTextField t3 = new JTextField(20);
        p.add(t3);
        JLabel idLabel = new JLabel("ID:");
        p.add(idLabel);
        JTextField t4 = new JTextField(20);
        p.add(t4);
        JLabel stockLabel = new JLabel("Stock:");
        p.add(stockLabel);
        JTextField t5 = new JTextField(20);
        p.add(t5);
        JLabel categoryLabel = new JLabel("Category:");
        p.add(categoryLabel);
        JTextField t6 = new JTextField(20);
        p.add(t6);
        JButton showBtn = new JButton("Show Products");
        showBtn.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                new VisualiseData(dbName);
            }
        });
        p.add(showBtn);
        f.setVisible(true);
    }
}