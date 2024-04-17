package lab;

import java.util.UUID;

public class Product {
    public String id;
    public String product;
    public int qty;
    public float cost;
    public float amt;
    public float tax;
    public float total;
    public String region;

    public static Product parseObjectFromString(String s) {
        String[] fields = s.split(" ");
        return new Product(fields[0], fields[1], Integer.parseInt(fields[2]), Float.parseFloat(fields[3]),
                Float.parseFloat(fields[4]), Float.parseFloat(fields[5]), Float.parseFloat(fields[6]),
                fields[7]);
    }

    @Override
    public String toString() {
        return this.id + " " + this.product + " " + this.qty + " " + this.cost + " " + this.amt + " " + this.tax
                + " " + this.total + " " + this.region;
    }

    public Product(String id, String product, int qty, float cost, float amt, float tax, float total, String region) {
        this.id = id;
        this.product = product;
        this.qty = qty;
        this.cost = cost;
        this.amt = amt;
        this.tax = tax;
        this.total = total;
        this.region = region;
    }

    public Product(String product, int qty, float cost, float amt, float tax, float total, String region) {
        id = UUID.randomUUID().toString();
        this.product = product;
        this.qty = qty;
        this.cost = cost;
        this.amt = amt;
        this.tax = tax;
        this.total = total;
        this.region = region;
    }
}