package lab.BranchOffice;

import javax.swing.*;
import lab.*;

public class BOGUI extends JFrame {
    public static int count = 1;
    public final String BO_DBNAME = "BO" + BOGUI.count;

    BOGUI() {
        Manager.createDb(BO_DBNAME);
        Manager.createProductTable(BO_DBNAME);
        Manager.sendOldDataToHO(BO_DBNAME);
        new BoManageProductGUI(BO_DBNAME);
        count = count + 1;
    }

    public static void main(String[] args) {
        new BOGUI();
        new BOGUI();
    }
}