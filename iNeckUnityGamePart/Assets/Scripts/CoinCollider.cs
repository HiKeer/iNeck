using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CoinCollider : MonoBehaviour
{
    [SerializeField] public int CoinCount;
    // Start is called before the first frame update
    void Start()
    {
        CoinCount = 0;
    }

    // Update is called once per frame
    void Update()
    {
        
    }
    private void CountPlus()
    {
        CoinCount ++;
    }
    /// <summary>
    /// OnTriggerEnter is called when the Collider other enters the trigger.
    /// </summary>
    /// <param name="other">The other Collider involved in this collision.</param>
    void OnTriggerEnter(Collider other)
    {
        if(other.tag == "Coin"){
            CountPlus();
        }
    }
}
