using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class RoadBlocksRunning : MonoBehaviour
{
    [SerializeField] float movespeed = 1.0f;
    // Start is called before the first frame update
    void Start()
    {
    }

    // Update is called once per frame
    void Update()
    {
        transform.position += new Vector3(0,0,-0.01f) * Time.deltaTime * movespeed;
    }
}
