from algopy import (
    Account,
    Bytes,
    GlobalState,
    String,
    Txn,
    UInt64,
    arc4,
    log,
    subroutine,
)
from algopy.arc4 import abimethod, baremethod


class simple_BPMN_choreography(arc4.ARC4Contract):

    def __init__(self) -> None:
        # Admin account
        self.admin = GlobalState(Account)
        
        self.party_a = GlobalState(Account("C3YYRKG4UNNWRGZAUZ5U5NEUSL5A23IKZE3LQNBWO64HJFBAQLLTS7QZCQ"))
        self.party_b = GlobalState(Account("VIIMQ37AU72TQM4KKAR76BDHG5DCO3HUUJYNVIZLMJBPXMXRQWPEAAWGZA"))
        self.party_c = GlobalState(Account("W6WNRQA3WUW7KR2UBQD4RSLSX6VD745Z62S4N6FPKWC36NDWO3NYIV7D6E"))  

        # Edge marking variables
        self.e0 = GlobalState(UInt64(0))
        self.e1 = GlobalState(UInt64(0))
        self.e2 = GlobalState(UInt64(0))
        self.e3 = GlobalState(UInt64(0))
        self.e4 = GlobalState(UInt64(0))
        self.e5 = GlobalState(UInt64(0))
        self.e6 = GlobalState(UInt64(0))

        # Message-specific variables
        self.msg1_payload_x = GlobalState(UInt64(0))
        self.msg2_payload_y = GlobalState(UInt64(0))
        self.msg4_payload_k = GlobalState(UInt64(0))
        self.msg3_payload_z = GlobalState(UInt64(0))

        # Locking variable
        self.locked = GlobalState(UInt64(0))  # 0 = unlocked, 1 = locked
        self.update_policy = GlobalState(UInt64(0))  # 0 = update disabled, 1 = update enabled

    @arc4.baremethod(create="allow")
    def create(self) -> None:
        """Initialize the choreography instance."""
        self.e0.value = UInt64(1)
        self.admin.value = Txn.sender
        self.update_policy.value = UInt64(1)
        self.locked.value = UInt64(0)
        log(Bytes(b"Choreography initialized successfully."))

    @subroutine
    def start1(self) -> UInt64:
        """Execute event start1."""
        if self.e0.value > UInt64(0):
            self.e0.value -= UInt64(1)
            self.e1.value += UInt64(1)
            return UInt64(1)
        return UInt64(0)

    @arc4.abimethod
    def task1(self, msg1_param_x: UInt64) -> None:
        assert self.locked.value == UInt64(0), "Contract is locked"
        assert self.e1.value > UInt64(0), "Task 1 not active."
        assert Txn.sender == self.party_a.value, "Only A can send msg1"
        self.e1.value -= UInt64(1)
        self.msg1_payload_x.value = msg1_param_x
        self.e2.value += UInt64(1)
        self.update_policy.value = UInt64(0)
        self.execute()

    @subroutine
    def xor1(self) -> UInt64:
        """Execute xor1."""
        if self.e2.value > UInt64(0):
            if self.msg1_payload_x.value >= UInt64(5):
                log(Bytes(b"Branching to task2"))
                self.e2.value -= UInt64(1)
                self.e3.value += UInt64(1)
            else:
                log(Bytes(b"Branching to end2"))
                self.e2.value -= UInt64(1)
                self.e5.value += UInt64(1)
            return UInt64(1)
        return UInt64(0)

    @arc4.abimethod
    def task2(self, msg4_param_k: UInt64) -> None:
        assert self.locked.value == UInt64(0), "Contract is locked"
        assert self.e3.value > UInt64(0), "Task 2 not active."
        assert Txn.sender == self.party_b.value, "Only B can send msg2"
        self.e3.value -= UInt64(1)
        self.msg4_payload_k.value = msg4_param_k
        self.e4.value += UInt64(1)
        self.execute()

    @subroutine
    def end1(self) -> UInt64:
        """Execute end1."""
        if self.e4.value > UInt64(0):
            log(Bytes(b"Process ended via end1"))
            self.e4.value -= UInt64(1)
            return UInt64(1)
        return UInt64(0)

    @arc4.abimethod
    def task3(self, msg3_param_z: UInt64) -> None:
        assert self.locked.value == UInt64(0), "Contract is locked"
        assert self.e5.value > UInt64(0), "Task 3 not active."
        assert Txn.sender == self.party_c.value, "Only B can send msg3"
        self.e5.value -= UInt64(1)
        self.msg3_payload_z.value = msg3_param_z
        self.e6.value += UInt64(1)
        self.execute()

    @subroutine
    def end2(self) -> UInt64:
        """Execute end2."""
        if self.e6.value > UInt64(0):
            log(Bytes(b"Process ended via end2"))
            self.e6.value -= UInt64(1)
            return UInt64(1)
        return UInt64(0)

    @baremethod(allow_actions=["UpdateApplication"])
    def update(self) -> None:
        assert Txn.sender == self.admin.value, "Only admin can update the contract"
        assert self.update_policy.value == UInt64(1), "Update is disabled"  # check the update policy
        self.locked.value = UInt64(1)  # Lock the contract
        log(Bytes(b"Contract updated successfully"))

    @arc4.abimethod
    def update_global_store(self) -> None:
        """Update the global store."""
        assert Txn.sender == self.admin.value, "Only admin can update the global store"
        self.locked.value = UInt64(0)  # Unlock the contract

        # Added variables
        self.e6.value = UInt64(0)
        self.msg4_payload_k.value = UInt64(0)
        self.msg3_payload_z.value = UInt64(0)
        self.party_c.value = Account("OWSIGW6NHIYMNMP7ZA53Z23GTRDXZYB3TGDPH5LH5TI3QBHDWIH775ZZLE")
        # Removed variables
        del self.msg2_payload_y.value
        log(Bytes(b"Contract variables updated successfully"))

    @arc4.abimethod(allow_actions=["DeleteApplication"])
    def delete(self) -> None:
        assert Txn.sender == self.admin.value, "Only admin can delete the contract"
        assert self.locked.value == UInt64(0), "Contract is locked"
        log(Bytes(b"XRay Choreography contract deleted successfully"))

    @subroutine
    def execute_one_rule(self) -> UInt64:
        if self.start1() != UInt64(0):
            return UInt64(1)
        if self.xor1() != UInt64(0):
            return UInt64(1)
        if self.end1() != UInt64(0):
            return UInt64(1)
        if self.end2() != UInt64(0):
            return UInt64(1)
        return UInt64(0)

    @arc4.abimethod
    def execute(self) -> UInt64:
        assert self.locked.value == UInt64(0), "Contract is locked"
        executed = True
        while executed:
            rule_executed = self.execute_one_rule()
            executed = rule_executed != UInt64(0)

        if (
            self.e0.value
            + self.e1.value
            + self.e2.value
            + self.e3.value
            + self.e4.value
            + self.e5.value
            + self.e6.value
            > UInt64(0)
        ):
            log(Bytes(b"The process instance is RUNNING"))
        else:
            log(Bytes(b"The process instance is COMPLETED"))
        return UInt64(1)
