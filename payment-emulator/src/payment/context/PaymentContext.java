package payment.context;

import payment.Payment;

import java.time.Instant;
import java.util.List;

public class PaymentContext {
    public Payment build(
            String customerId,
            double amount,
            String cardType,
            String productType,
            String email,
            String deviceId,
            String merchantId,
            String merchantType,
            String merchantRisk,
            String location,
            Instant time,
            String ip,
            boolean authenticated,
            List<Payment> previous
    ) {
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
        long secondsSincePrevious = 0;
        if (!previous.isEmpty()) {
            Payment last = previous.get(previous.size() - 1);
            locationChanged = !last.location().equals(location);
            secondsSincePrevious = time.getEpochSecond() - last.time().getEpochSecond();
        }
        return new Payment(
                customerId,
                amount,
                usualAmount,
                amountComparedToUsual,
                cardType,
                productType,
                email,
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
                authenticated,
                secondsSincePrevious,
                null
        );
    }
}
