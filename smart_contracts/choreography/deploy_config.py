import logging
import algokit_utils

logger = logging.getLogger(__name__)


def deploy() -> None:
    from smart_contracts.artifacts.choreography.simple_BPMN_choreography_client import (
        SimpleBPMNChoreographyFactory,
    )

    algorand = algokit_utils.AlgorandClient.from_environment()
    deployer = algorand.account.from_environment("DEPLOYER")

    # Deploy the smart contract
    factory = algorand.client.get_typed_app_factory(
        SimpleBPMNChoreographyFactory, default_sender=deployer.address
    )

    app_client, result = factory.deploy(
        on_update=algokit_utils.OnUpdate.AppendApp,
        on_schema_break=algokit_utils.OnSchemaBreak.AppendApp,
    )

    # Fund the smart contract with 1 ALGO on creation or replacement
    if result.operation_performed in [
        algokit_utils.OperationPerformed.Create,
        algokit_utils.OperationPerformed.Replace,
    ]:
        algorand.send.payment(
            algokit_utils.PaymentParams(
                sender=deployer.address,
                receiver=app_client.app_address,
                amount=algokit_utils.AlgoAmount(algo=1),
            )
        )

    logger.info(
        f"Deployed BPMN Choreography contract {app_client.app_name} "
        f"({app_client.app_id}) at address {app_client.app_address}"
    )

    # Optionally call any method here (e.g., task1 or execute)
    # Example:
    # app_client.send.execute()
