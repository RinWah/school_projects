public interface PaymentService {
    boolean charge(String account, double amount);
    boolean refund(String account);
}
public interface InventoryService {
    int getStock(String itemId);
    boolean reserve(String itemId, int quantity);
}
public class OrderProcessor {
    private PaymentService paymentService;
    private InventoryService inventoryService;
    public OrderProcessor(PaymentService ps, InventoryService is) {
        this.paymentService = ps;
        this.inventoryService = is;
    }
    public String placeOrder(String account, String itemId, 
                            int quantity, double unitPrice) {
        if (quantity <= 0) {
            throw new IllegalArgumentException(
                "Quantity must be positive");
        }
        int stock = inventoryService.getStock(itemId);
        if (stock < quantity) {
            return "OUT_OF_STOCK";
        }
        double total = quantity * unitPrice;
        boolean charged = paymentService.charge(account, total);
        if (!charged) {
            return "PAYMENT_FAILED";
        }
        boolean reserved = inventoryService.reserve(itemId, quantity);
        if (!reserved) {
            paymentService.refund(account);
            return "RESERVE_FAILED";
        }
        return "SUCCESS";
    }
}