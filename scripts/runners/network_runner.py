import logging
import uuid
from decimal import Decimal
from services.neo4j.sfo_network_pathfinder import SFONetworkPathfinder
from services.deal.club_deal_manager import ClubDealManager
from services.external.salesforce_adapter import SalesforceAdapter

logger = logging.getLogger(__name__)

def find_connection(target: str, office_id: str = None):
    """
    CLI Handler for pathfinding.
    """
    oid = uuid.UUID(office_id) if office_id else uuid.uuid4()
    pf = SFONetworkPathfinder()
    res = pf.find_shortest_connection(oid, target)
    
    print("\n" + "="*50)
    print("          NETWORK CONNECTION FINDER")
    print("="*50)
    print(f"Target:           {target}")
    print(f"Path Length:      {res['path_length']}")
    print(f"Intermediary:     {res['intermediary']}")
    print("-" * 50)
    print(f"Status:           {res['status']}")
    print("="*50 + "\n")

def spin_up_club(name: str, total: float, commit: float):
    """
    CLI Handler for club deal creation.
    """
    mgr = ClubDealManager()
    invitees = [uuid.uuid4() for _ in range(3)]
    res = mgr.create_club_deal(name, total, commit, invitees)
    
    print("\n" + "="*50)
    print("          CLUB DEAL FORMATION")
    print("="*50)
    print(f"Deal Name:        {name}")
    print(f"Total Size:       ${total:,.2f}")
    print(f"Commitment:       ${commit:,.2f}")
    print(f"Seeking:          ${res['syndication_required']:,.2f}")
    print("-" * 50)
    print(f"Invites Sent:     {res['invites_sent']} (Legacy Network)")
    print(f"Deal ID:          {res['deal_id']}")
    print("="*50 + "\n")

def sync_crm(office_id: str):
    """
    CLI Handler for CRM sync.
    """
    adapter = SalesforceAdapter()
    oid = uuid.UUID(office_id)
    contacts = adapter.sync_contacts(oid)
    
    print("\n" + "="*50)
    print("          SALESFORCE CRM SYNC")
    print("="*50)
    print(f"Office ID:        {office_id}")
    print(f"Sync Count:       {len(contacts)}")
    print("-" * 50)
    for c in contacts:
        print(f"- {c['name']} ({c['org']}) | Domain: {c['domain']}")
    print("="*50 + "\n")
