import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
public class OrderProcessorTest {
    private PaymentService ps;
    private InventoryService is;
    private OrderProcessor op;
    @BeforeEach
    void setUp() {
        ps = mock(PaymentService.class);
        is = mock(InventoryService.class);
        op = new OrderProcessor(ps, is);
    }
    @Test 
    public void testSuccessfulOrder() {
        when(is.getStock("ITEM1")).thenReturn(10);
        when(ps.charge("ACC1", 50.0)).thenReturn(true);
        when(is.reserve("ITEM1", 5)).thenReturn(true);
        OrderProcessor op = new OrderProcessor(ps, is);
        assertEquals("SUCCESS",
            op.placeOrder("ACC1", "ITEM1", 5, 10.0));
        verify(is).reserve("ITEM1", 5);
}
    @Test 
    void testOutOfStock() {
        when(is.getStock("ITEM1")).thenReturn(2);
        assertEquals("OUT_OF_STOCK", op.placeOrder("ACC1", "ITEM1", 5, 10.0));
        // verify payment change was not attempted
        verify(ps, never()).charge(anyString(), anyDouble());
    }
    @Test 
    void testPaymentFailed() {
        when(is.getStock("ITEM1")).thenReturn(10);
        when(ps.charge("ACC1", 50.0)).thenReturn(false);
        assertEquals("PAYMENT_FAILED", op.placeOrder("ACC1", "ITEM1", 5, 10.0));
        // requirement: verify reserve() is not called when payment fails
        verify(is, never()).reserve(anyString(), anyInt());
    }
    @Test 
    void testReserveFailed() {
        when(is.getStock("ITEM1")).thenReturn(10);
        when(ps.charge("ACC1", 50.0)).thenReturn(true);
        when(is.reserve("ITEM1", 5)).thenReturn(false);
        assertEquals("RESERVE_FAILED", op.placeOrder("ACC1", "ITEM1", 5, 10.0));
        // requirement: verify refund() is called when reservation fails
        verify(ps).refund("ACC1");
    }
    @Test 
    void testInvalidQuantity() {
        assertThrows(IllegalArgumentException.class, () -> {
            op.placeOrder("ACC1", "ITEM1", 0, 10.0);
        });
    }
}