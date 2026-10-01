package payment;

import payment.context.PaymentContext;
import payment.fraud.FraudCheck;
import payment.fraud.FraudEngine;
import payment.history.PaymentHistory;

import java.time.Instant;
import java.util.List;

public class PaymentSystem {
    private final PaymentHistory paymentHistory;
    private final PaymentContext paymentContext;
    private final FraudCheck fraudCheck;

    public PaymentSystem() {
        this(new PaymentHistory(), new PaymentContext(), new FraudEngine());
    }

    public PaymentSystem(PaymentHistory paymentHistory, PaymentContext paymentContext, FraudCheck fraudCheck) {
        this.paymentHistory = paymentHistory;
        this.paymentContext = paymentContext;
        this.fraudCheck = fraudCheck;
    }

    public Payment pay(
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
            boolean authenticated
    ) {
        List<Payment> previous = paymentHistory.previous(customerId);
        Payment payment = paymentContext.build(
                customerId,
                amount,
                cardType,
                productType,
                email,
                deviceId,
                merchantId,
                merchantType,
                merchantRisk,
                location,
                time,
                ip,
                authenticated,
                previous
        );
        payment = payment.withDecision(fraudCheck.checkPaymentForFraud(payment));
        paymentHistory.add(customerId, payment);
        return payment;
    }

    public List<Payment> history(String customerId) {
        return paymentHistory.history(customerId);
    }
}
