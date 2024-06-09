using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class WorldGenerator : MonoBehaviour
{
    [SerializeField] float EvnMoveSpeed = 2.0f;
    [SerializeField] Transform StartingPoint;
    [SerializeField] Transform EndPoint;
    [SerializeField] GameObject[] RoadBlocks;
    [SerializeField] GameObject[] CoinBlocks;
    [SerializeField] Transform[] SpawnCoinPoints;
    Vector3 MoveDirection;
    float blockLength;
    [SerializeField] int cul = 0;


    // Start is called before the first frame update
    void Start()
    {
        Vector3 NextBlockPosition = StartingPoint.position;
        int i =1;
        MoveDirection = (EndPoint.position - StartingPoint.position).normalized;
        float EndPointDistance = Vector3.Distance(StartingPoint.position,EndPoint.position);
        while(Vector3.Distance(StartingPoint.position,NextBlockPosition)<EndPointDistance){
            GameObject newBlock = SpawnNewBlock(NextBlockPosition,MoveDirection);
            blockLength = newBlock.GetComponent<Renderer>().bounds.size.z;
            NextBlockPosition += MoveDirection * blockLength;
            newBlock.name = $"{i}";
            i++;
        }
    }

    // Update is called once per frame
    void Update()
    {
        
    }
    GameObject SpawnNewBlock(Vector3 SpawnPosition,Vector3 MoveDir){
            int pick = Random.Range(0,RoadBlocks.Length);
            GameObject pickedBlock = RoadBlocks[pick];
            GameObject newBlock = Instantiate(pickedBlock);
            newBlock.transform.position = SpawnPosition;
            MovementComp moveComp = newBlock.GetComponent<MovementComp>();
            if(moveComp != null){
                moveComp.SetMoveDir(MoveDir);
                moveComp.SetMoveSpeed(EvnMoveSpeed);
                moveComp.SetDestination(EndPoint.position);
            }
            return newBlock;
    }

    private void OnTriggerExit(Collider other)
    {
        if(other.gameObject != null){
            GameObject newBlock = SpawnNewBlock(other.transform.position,MoveDirection);
            float newBlockHalfWidth = newBlock.GetComponent<Renderer>().bounds.size.z/2f;
            float previoesBlockHalfWidth = other.GetComponent<Renderer>().bounds.size.z/2f;
            Vector3 newBlockSpawnOffset = -(newBlockHalfWidth + previoesBlockHalfWidth)*MoveDirection;
            newBlock.transform.position += newBlockSpawnOffset;
            newBlock.name = "newly block";
            if(cul == 2 ){
                GameObject newCoin = SpawnNewCoin(MoveDirection);
                newCoin.transform.position += newBlockSpawnOffset;
                cul = 0;
            }else if(cul < 2 ){
                cul++;
            };
        }
    }

    private GameObject SpawnNewCoin(Vector3 MoveDir)
    {
        int pick = Random.Range(0,SpawnCoinPoints.Length);
        GameObject pickedPoint = CoinBlocks[pick];
        GameObject newCoin = Instantiate(pickedPoint);
        newCoin.transform.position = SpawnCoinPoints[pick].transform.position;
        MovementComp moveComp = newCoin.GetComponent<MovementComp>();
            if(moveComp != null){
                moveComp.SetMoveDir(MoveDir);
                moveComp.SetMoveSpeed(EvnMoveSpeed);
                moveComp.SetDestination(EndPoint.position);
            }
        return newCoin;
    }
}
