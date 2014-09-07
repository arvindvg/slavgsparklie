from tests.test_helper import *
from braintree.test.credit_card_numbers import CreditCardNumbers

class TestCreditCard(unittest.TestCase):
    def test_find_with_verification_id(self):
        customer = Customer.create({
            "credit_card": {
                "number": CreditCardNumbers.FailsSandboxVerification.MasterCard,
                "expiration_date": "05/2012",
                "cardholder_name": "Tom Smith",
                "options": {"verify_card": True}
        }})

        created_verification = customer.credit_card_verification
        found_verification = CreditCardVerification.find(created_verification.id)
        self.assertEquals(created_verification, found_verification)

    def test_verification_not_found(self):
        self.assertRaises(NotFoundError, CreditCardVerification.find,
          "invalid-id")

    def test_card_type_indicators(self):
        cardholder_name = "Tom %s" % randint(1, 10000)
        Customer.create({"credit_card": {
            "cardholder_name": cardholder_name,
            "expiration_date": "10/2012",
            "number": CreditCardNumbers.CardTypeIndicators.Unknown,
            "options": {"verify_card": True}
        }})
        found_verifications = CreditCardVerification.search(
            CreditCardVerificationSearch.credit_card_cardholder_name == cardholder_name
        )

        self.assertEqual(CreditCard.Prepaid.Unknown, found_verifications.first.credit_card['prepaid'])
        self.assertEqual(CreditCard.Debit.Unknown, found_verifications.first.credit_card['debit'])
        self.assertEqual(CreditCard.Commercial.Unknown, found_verifications.first.credit_card['commercial'])
        self.assertEqual(CreditCard.Healthcare.Unknown, found_verifications.first.credit_card['healthcare'])
        self.assertEqual(CreditCard.Payroll.Unknown, found_verifications.first.credit_card['payroll'])
        self.assertEqual(CreditCard.DurbinRegulated.Unknown, found_verifications.first.credit_card['durbin_regulated'])
        self.assertEqual(CreditCard.CardTypeIndicator.Unknown, found_verifications.first.credit_card['issuing_bank'])
        self.assertEqual(CreditCard.CardTypeIndicator.Unknown, found_verifications.first.credit_card['country_of_issuance'])

