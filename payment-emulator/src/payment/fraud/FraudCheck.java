package payment.fraud;

import payment.Payment;

public interface FraudCheck {
    String checkPaymentForFraud(Payment payment);
}
