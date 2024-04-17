package lab;

import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import io.github.cdimascio.dotenv.Dotenv;

import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.Statement;

public class Manager {

    public final static String HO_QUEUE = "ho_queue";
    public final static String HO_DBNAME = "HO";
    // Global database connection variables
    static Dotenv dotenv = Dotenv.load();

    private static String url = dotenv.get("DB_URL");
    private static String username = dotenv.get("DB_USERNAME");;
    private static String password = dotenv.get("DB_PASSWORD");;

    public static void createDb(String dbName) {
        try {
            // Establish connection to MySQL server
            java.sql.Connection con = DriverManager.getConnection(url + dbName, username, password);
            Statement stmt = con.createStatement();

            stmt.execute("CREATE DATABASE if not exists " + dbName);
            System.out.println("success");
            // Close the connection
            con.close();
        } catch (Exception e) {
            // Print error message if database creation fails
            System.out.println("error in creating data base " + dbName);
            System.out.println(e);
        }
    }

    // Creates a product table
    public static void createProductTable(String dbName) {
        try {
            // Establish connection to the specified database
            java.sql.Connection con = DriverManager.getConnection(url + dbName, username, password);
            // Create a statement for executing SQL queries
            Statement stmt = con.createStatement();
            String sql = "CREATE TABLE IF NOT EXISTS product (" +
                    "id VARCHAR(100) PRIMARY KEY , " +
                    "product VARCHAR(50)," +
                    "qty INT," +
                    "cost FLOAT," +
                    "amt FLOAT," +
                    "tax FLOAT," +
                    "total FLOAT," +
                    "region VARCHAR(50)" +
                    ")";
            stmt.executeUpdate(sql);
            con.close();
        } catch (Exception e) {
            System.out.println("error in creating the product table in database " + dbName);
            System.out.println(e);
        }
    }

    // Sends a Product object to be stored in the specified database
    public static void sendToDB(Product p, String dbName) {
        try {
            java.sql.Connection con = DriverManager.getConnection(url + dbName, username, password);
            String sql = "replace into product (id, product, qty, cost, amt, tax, total, region) values (?, ?, ?, ?, ?, ?, ?, ?);";
            PreparedStatement stmt = con.prepareStatement(sql);
            stmt.setString(1, p.id);
            stmt.setString(2, p.product);
            stmt.setInt(3, p.qty);
            stmt.setFloat(4, p.cost);
            stmt.setFloat(5, p.amt);
            stmt.setFloat(6, p.tax);
            stmt.setFloat(7, p.total);
            stmt.setString(8, p.region);
            stmt.executeUpdate();
            con.close();
        } catch (Exception e) {
            System.out.println("failed to send the product: " + p.product);
            System.out.println(e);
        }
    }

    // Retrieves all products from the specified database
    public static String[][] getAllProducts(String dbName) {
        String[][] products = new String[100][9];
        int i = 0;
        try {
            java.sql.Connection con = DriverManager.getConnection(url + dbName, username, password);
            Statement stmt = con.createStatement();
            String sql = "SELECT * FROM product;";
            ResultSet rs = stmt.executeQuery(sql);
            while (rs.next()) {
                products[i][0] = rs.getString(1);
                products[i][1] = rs.getString(2);
                products[i][2] = Integer.toString(rs.getInt(3));
                products[i][3] = Float.toString(rs.getFloat(4));
                products[i][4] = Float.toString(rs.getFloat(5));
                products[i][5] = Float.toString(rs.getFloat(6));
                products[i][6] = Float.toString(rs.getFloat(7));
                products[i][7] = rs.getString(8);
                i++;
            }
        } catch (Exception e) {
            System.out.println("Error in retrieving data from " + dbName);
            System.out.println(e);
        }
        String[][] products1 = new String[i][9];
        for (int j = 0; j < i; j++) {
            products1[j][0] = products[j][0];
            products1[j][1] = products[j][1];
            products1[j][2] = products[j][2];
            products1[j][3] = products[j][3];
            products1[j][4] = products[j][4];
            products1[j][5] = products[j][5];
            products1[j][6] = products[j][6];
            products1[j][7] = products[j][7];
        }
        return products1;
    }

    // Sends a product to the Head Office via RabbitMQ for processing
    public static void sendToHO(Product p) {
        try {
            ConnectionFactory factory = new ConnectionFactory();
            factory.setHost("localhost");
            // Establish a connection to RabbitMQ
            Connection connection = factory.newConnection();
            // Create a channel for communication
            Channel channel = connection.createChannel();
            // Declare the queue for HO
            channel.queueDeclare(HO_QUEUE, false, false, false, null);
            // Construct the message to be sent to HO (using the "ADD" flag to indicate
            // addition of a product)
            String msg = "ADD" + p.toString();
            // Publish the message to the HO queue
            channel.basicPublish("", HO_QUEUE, null, msg.getBytes());
        } catch (Exception e) {
            System.out.println("error sending data to HO ");
            System.out.println(e);
        }
    }

    // Sends old data from the specified database to Head Office
    public static void sendOldDataToHO(String dbName) {
        try {
            java.sql.Connection con = DriverManager.getConnection(url + dbName, username, password);
            Statement stmt = con.createStatement();
            String sql = "SELECT * FROM product;";
            ResultSet product = stmt.executeQuery(sql);
            while (product.next()) {
                String id = product.getString(1);
                String productname = product.getString(2);
                float qty = product.getInt(3);
                float cost = product.getFloat(4);
                float amt = product.getFloat(5);
                float tax = product.getFloat(6);
                float total = product.getFloat(7);
                String region = product.getString(8);
                Product p = new Product(id, productname, (int) qty, cost, amt, tax, total, region);
                sendToHO(p);
            }
        } catch (Exception e) {
            System.out.println(e);
        }
    }

    public static void execQuery(String sql, String dbName) {
        try {
            java.sql.Connection con = DriverManager.getConnection(url + dbName, username, password);
            Statement stmt = con.createStatement();
            stmt.executeUpdate(sql);
        } catch (Exception e) {
            System.out.println("error in executing  query : " + sql);
            System.out.println(e);
        }
    }

    public static void removeFromBD(String id, String dbName) {
        String sql = "DELETE FROM product WHERE id = '" + id + "';";
        execQuery(sql, dbName);
    }

    public static void removeFromHO(String id) {
        try {
            ConnectionFactory factory = new ConnectionFactory();
            factory.setHost("localhost");
            Connection connection = factory.newConnection();
            Channel channel = connection.createChannel();
            channel.queueDeclare(HO_QUEUE, false, false, false, null);
            channel.basicPublish("", HO_QUEUE, null, ("DEL" + id).getBytes());
        } catch (Exception e) {
            System.out.println("error sending data to HO ");
            System.out.println(e);
        }
    }
}