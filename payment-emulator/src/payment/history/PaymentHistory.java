package payment.history;

import payment.Payment;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class PaymentHistory {
    private final Map<String, List<Payment>> payments = new HashMap<>();

    public List<Payment> previous(String customerId) {
        return payments.computeIfAbsent(customerId, id -> new ArrayList<>());
    }

    public void add(String customerId, Payment payment) {
        previous(customerId).add(payment);
    }

    public List<Payment> history(String customerId) {
        return List.copyOf(payments.getOrDefault(customerId, List.of()));
    }
}
