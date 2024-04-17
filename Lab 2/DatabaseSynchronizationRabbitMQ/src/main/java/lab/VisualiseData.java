package lab;

import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class VisualiseData extends JFrame {
    public final String dbName;

    public VisualiseData(String dbName) {
        this.dbName = dbName;
        this.setTitle("product table from " + dbName);
        Object[][] products = Manager.getAllProducts(dbName);
        String column[] = { "id", "product", "qty", "cost", "amt", "tax", "total", "region" };
        DefaultTableModel model = new DefaultTableModel(products, column);
        JTable table = new JTable(model);
        table.setSelectionMode(javax.swing.ListSelectionModel.SINGLE_SELECTION);
        if (dbName != "HO") {
            JButton button = new JButton("Remove");
            button.addActionListener(new ActionListener() {
                @Override
                public void actionPerformed(ActionEvent ae) {
                    // check for selected row first
                    if (table.getSelectedRow() != -1) {
                        // remove selected row from the model
                        String id = table.getValueAt(table.getSelectedRow(), 0).toString();
                        Manager.removeFromBD(id, dbName);
                        Manager.removeFromHO(id);
                        model.removeRow(table.getSelectedRow());
                        JOptionPane.showMessageDialog(null, "Selected row deleted successfully");
                    }
                }
            });
            add(button, BorderLayout.SOUTH);
        }
        add(new JScrollPane(table), BorderLayout.CENTER);
        // Set the close operation to dispose the frame
        setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        setSize(400, 300);
        setLocationRelativeTo(null);
        setVisible(true);
    }
}