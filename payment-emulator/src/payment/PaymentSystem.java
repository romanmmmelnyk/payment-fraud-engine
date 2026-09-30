package payment;

import java.time.Instant;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class PaymentSystem {
    private final Map<String, List<Payment>> payments = new HashMap<>();

    public Payment pay(
            String customerId,
            double amount,
            String deviceId,
            String merchantId,
            String merchantType,
            String merchantRisk,
            String location,
            Instant time,
            String ip,
            boolean authenticated
    ) {
        List<Payment> previous = payments.computeIfAbsent(customerId, id -> new ArrayList<>());
        double usualAmount = 0;
        double amountComparedToUsual = 0;
        if (!previous.isEmpty()) {
            double sum = 0;
            for (Payment payment : previous) {
                sum += payment.amount();
            }
            usualAmount = sum / previous.size();
            amountComparedToUsual = amount - usualAmount;
        }
        boolean deviceNew = true;
        boolean merchantNew = true;
        for (Payment payment : previous) {
            if (payment.deviceId().equals(deviceId)) {
                deviceNew = false;
            }
            if (payment.merchantId().equals(merchantId)) {
                merchantNew = false;
            }
        }
        boolean locationChanged = false;
        if (!previous.isEmpty()) {
            locationChanged = !previous.get(previous.size() - 1).location().equals(location);
        }
        Payment payment = new Payment(
                customerId,
                amount,
                usualAmount,
                amountComparedToUsual,
                deviceId,
                deviceNew,
                merchantId,
                merchantNew,
                merchantType,
                merchantRisk,
                location,
                locationChanged,
                time,
                previous.size(),
                ip,
                authenticated
        );
        previous.add(payment);
        return payment;
    }

    public List<Payment> history(String customerId) {
        return List.copyOf(payments.getOrDefault(customerId, List.of()));
    }
}
