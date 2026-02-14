from ciphers.test_cipher import SimpleXORCipher
from core.agent import CipherAuditAgent

cipher = SimpleXORCipher()
agent = CipherAuditAgent(cipher)
report = agent.run_full_audit()
print(report)