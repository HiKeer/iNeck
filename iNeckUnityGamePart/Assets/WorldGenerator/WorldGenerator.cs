using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class WorldGenerator : MonoBehaviour
{
    [SerializeField] Transform StartingPoint;
    [SerializeField] Transform EndPoint;
    [SerializeField] GameObject[] RoadBlocks;

    // Start is called before the first frame update
    void Start()
    {
        Vector3 NextBlockPosition = StartingPoint.position;
        float EndPointDistance = Vector3.Distance(StartingPoint.position,EndPoint.position);
        while(Vector3.Distance(StartingPoint.position,NextBlockPosition)<EndPointDistance){
            int pick = Random.Range(0,RoadBlocks.Length);
            GameObject pickedBlock = RoadBlocks[pick];
            GameObject newBlock = Instantiate(pickedBlock);
            newBlock.transform.position = NextBlockPosition;
            float blockLength = newBlock.GetComponent<Renderer>().bounds.size.z;
            NextBlockPosition += (EndPoint.position - StartingPoint.position).normalized * blockLength;
        }
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
